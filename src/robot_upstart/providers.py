# Software License Agreement (BSD)
#
# @author    Mike Purvis <mpurvis@clearpathrobotics.com>
# @copyright (c) 2015, Clearpath Robotics, Inc., All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that
# the following conditions are met:
# * Redistributions of source code must retain the above copyright notice, this list of conditions and the
#   following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
#   following disclaimer in the documentation and/or other materials provided with the distribution.
# * Neither the name of Clearpath Robotics nor the names of its contributors may be used to endorse or
#   promote products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
These classes implement the translation from user-intended behaviours
as specified in the state of the Job class to the system-specific configuration
files. At present, there is only an upstart configuration, but similar providers
could be defined for systemd, supervisor, launchd, or other systems.
"""

import em
import os
import io

from catkin.find_in_workspaces import find_in_workspaces


def detect_provider():
    cmd = open('/proc/1/cmdline', 'rb').read().split(b'\x00')[0]
    print(os.path.realpath(cmd))
    if b'systemd' in os.path.realpath(cmd):
        return Systemd
    return Upstart


class Generic(object):
    """ Provides only a common constructor for the moment, but as further
        providers are implemented, may provide a place to store configuration
        common to them. """

    def __init__(self, root, job):
        """ Construct a new Provider.

        :param root: The filesystem location to prefix all file-install
            commands with.
        :type root: str
        :param job: The job definition to transform to a set of system files.
        :type job: :py:class:robot_upstart.Job
        """
        self.root = root
        self.job = job

        # Recipe structure which is serialized to yaml and passed to the mutate_files script.
        self.installation_files = {}

        # Bare list of files, stored in the .installed_files manifest file.
        self.installed_files_set = set()

    def _add_job_files(self):
        # Make up list of files to copy to system locations.
        for filename in self.job.files:
            dest_filename = os.path.join(self.job.job_path, os.path.basename(filename))
            if self.job.symlink:
                self.installation_files[dest_filename] = {"symlink": filename}
            else:
                with open(filename) as f:
                    self.installation_files[dest_filename] = {"content": f.read()}

    def _load_installed_files_set(self):
        self.installed_files_set_location = os.path.join(self.job.job_path, ".installed_files")
        if os.path.exists(self.installed_files_set_location):
            with open(self.installed_files_set_location) as f:
                self.installed_files_set.update(f.read().split("\n"))


class Upstart(Generic):
    """ The Upstart implementation places the user-specified files in ``/etc/ros/DISTRO/NAME.d``,
    and creates an upstart job configuration in ``/etc/init/NAME.d``. Two additional
    helper scripts are created for starting and stopping the job, places in
    ``/usr/sbin``.
    """

    def generate_install(self):
        # Default for Upstart is /etc/ros/DISTRO/JOBNAME.d
        self._set_job_path()

        # User-specified launch files.
        self._add_job_files()

        # This is optional to support the old --augment flag where a "job" only adds
        # launch files to an existing configuration.
        if (self.job.generate_system_files):
            # Share a single instance of the empy interpreter.
            self.interpreter = em.Interpreter(globals=self.job.__dict__.copy())

            self.installation_files[os.path.join(self.root, "etc/init", self.job.name + ".conf")] = {
                "content": self._fill_template("templates/job.conf.em"), "mode": 0o644}
            self.installation_files[os.path.join(self.root, "usr/sbin", self.job.name + "-start")] = {
                "content": self._fill_template("templates/job-start.em"), "mode": 0o755}
            self.installation_files[os.path.join(self.root, "usr/sbin", self.job.name + "-stop")] = {
                "content": self._fill_template("templates/job-stop.em"), "mode": 0o755}
            self.interpreter.shutdown()

        # Add an annotation file listing what has been installed. This is a union of what's being
        # installed now with what has been installed previously, so that an uninstall should remove
        # all of it. A more sophisticated future implementation could track contents or hashes and
        # thereby warn users when a new installation is stomping a change they have made.
        self._load_installed_files_set()
        self.installed_files_set.update(list(self.installation_files.keys()))

        # Remove the job directory. This will fail if it is not empty, and notify the user.
        self.installed_files_set.add(self.job.job_path)

        # Remove the annotation file itself.
        self.installed_files_set.add(self.installed_files_set_location)

        self.installation_files[self.installed_files_set_location] = {
            "content": "\n".join(self.installed_files_set)}

        return self.installation_files

    def post_install(self):
        return

    def generate_uninstall(self):
        self._set_job_path()
        self._load_installed_files_set()

        for filename in self.installed_files_set:
            self.installation_files[filename] = {"remove": True}

        return self.installation_files

    def _set_job_path(self):
        self.job.job_path = os.path.join(
            self.root, "etc/ros", self.job.rosdistro, self.job.name + ".d")

    def _fill_template(self, template):
        self.interpreter.output = io.StringIO()
        self.interpreter.reset()
        with open(find_in_workspaces(project="robot_upstart", path=template)[0]) as f:
            self.interpreter.file(f)
            return self.interpreter.output.getvalue()


class Systemd(Generic):
    """ The Systemd implementation places the user-specified files in ``/etc/ros/DISTRO/NAME.d``,
    and creates an systemd job configuration in ``/lib/systemd/system/NAME.d``. Two additional
    helper scripts are created for starting and stopping the job, places in
    ``/usr/sbin``.
    To detect which system you're using run: ps -p1 | grep systemd && echo systemd || echo upstart
    """

    def generate_install(self):
        # Default is /etc/ros/DISTRO/JOBNAME.d
        self._set_job_path()

        # User-specified launch files.
        self._add_job_files()

        # This is optional to support the old --augment flag where a "job" only adds
        # launch files to an existing configuration.
        if self.job.generate_system_files:
            # Share a single instance of the EmPy interpreter.
            self.interpreter = em.Interpreter(globals=self.job.__dict__.copy())

            self.installation_files[os.path.join(self.root, "lib/systemd/system", self.job.name + ".service")] = {
                "content": self._fill_template("templates/systemd_job.conf.em"), "mode": 0o644}
            self.installation_files[os.path.join(self.root, "etc/systemd/system/multi-user.target.wants",
                                                 self.job.name + ".service")] = {
                "symlink": os.path.join(self.root, "lib/systemd/system/", self.job.name + ".service")}
            self.installation_files[os.path.join(self.root, "usr/sbin", self.job.name + "-start")] = {
                "content": self._fill_template("templates/job-start.em"), "mode": 0o755}
            self.installation_files[os.path.join(self.root, "usr/sbin", self.job.name + "-stop")] = {
                "content": self._fill_template("templates/job-stop.em"), "mode": 0o755}
            self.interpreter.shutdown()

        # Add an annotation file listing what has been installed. This is a union of what's being
        # installed now with what has been installed previously, so that an uninstall should remove
        # all of it. A more sophisticated future implementation could track contents or hashes and
        # thereby warn users when a new installation is stomping a change they have made.
        self._load_installed_files_set()
        self.installed_files_set.update(list(self.installation_files.keys()))

        # Remove the job directory. This will fail if it is not empty, and notify the user.
        self.installed_files_set.add(self.job.job_path)

        # Remove the annotation file itself.
        self.installed_files_set.add(self.installed_files_set_location)

        self.installation_files[self.installed_files_set_location] = {
            "content": "\n".join(self.installed_files_set)}

        return self.installation_files

    def post_install(self):
        print("** To complete installation please run the following command:")
        print(" sudo systemctl daemon-reload" +
              " && sudo systemctl start " + self.job.name)

    def generate_uninstall(self):
        self._set_job_path()
        self._load_installed_files_set()

        for filename in self.installed_files_set:
            self.installation_files[filename] = {"remove": True}

        return self.installation_files

    def _set_job_path(self):
        self.job.job_path = os.path.join(
            self.root, "etc/ros", self.job.rosdistro, self.job.name + ".d")

    def _fill_template(self, template):
        self.interpreter.output = io.StringIO()
        self.interpreter.reset()
        with open(find_in_workspaces(project="robot_upstart", path=template)[0]) as f:
            self.interpreter.file(f)
            return self.interpreter.output.getvalue()
        self.set_job_path()
