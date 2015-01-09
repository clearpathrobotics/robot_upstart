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
import StringIO

from catkin.find_in_workspaces import find_in_workspaces


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


class Upstart(Generic):
    """ The Upstart implementation places the user-specified files in ``/etc/ros/DISTRO/NAME.d``,
    and creates an upstart job configuration in ``/etc/init/NAME.d``. Two additional
    helper scripts are created for starting and stopping the job, places in
    ``/usr/sbin``.
    """

    def generate(self):
        self.job.job_path = os.path.join(self.root, "etc/ros",
                self.job.rosdistro, self.job.name + ".d")

        # Make up list of files to copy to system locations.
        installation_files = {}
        for filename in self.job.files:
            with open(filename) as f:
                dest_filename = os.path.join(self.job.job_path, os.path.basename(filename))
                installation_files[dest_filename] = {"content": f.read()}

        # This is optional to support the old --augment flag where a "job" only adds
        # launch files to an existing configuration.
        if (self.job.generate_system_files):
            # Share a single instance of the empy interpreter.
            self.interpreter = em.Interpreter(globals=self.job.__dict__.copy())

            installation_files[os.path.join(self.root, "etc/init", self.job.name + ".conf")] = {
                "content": self._fill_template("templates/job.conf.em"), "mode": 644}
            installation_files[os.path.join(self.root, "usr/sbin", self.job.name + "-start")] = {
                "content": self._fill_template("templates/job-start.em"), "mode": 755}
            installation_files[os.path.join(self.root, "usr/sbin", self.job.name + "-stop")] = {
                "content": self._fill_template("templates/job-stop.em"), "mode": 755}
            self.interpreter.shutdown()

        return installation_files

    def _fill_template(self, template):
        self.interpreter.output = StringIO.StringIO()
        self.interpreter.reset()
        with open(find_in_workspaces(project="robot_upstart", path=template)[0]) as f:
            self.interpreter.file(f)
            return self.interpreter.output.getvalue()
