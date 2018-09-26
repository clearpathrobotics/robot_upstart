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
This file defines the Job class, which is the primary code API to robot_upstart.
"""

import getpass
import os
import pickle
import subprocess
from glob import glob as glob_files

from catkin.find_in_workspaces import find_in_workspaces

import providers


class Job(object):
    """ Represents a ROS configuration to launch on machine startup. """

    def __init__(self, name="ros", interface=None, user=None, workspace_setup=None,
                 rosdistro=None, master_uri=None, log_path=None):
        """Construct a new Job definition.

        :param name: Name of job to create. Defaults to "ros", but you might
            prefer to use the name of your platform.
        :type name: str
        :param interface: Network interface to bring ROS up with. If specified,
            the job will come up with that network interface, and ROS_IP will be set
            to that interface's IP address. If unspecified, the job will come up
            on system startup, and ROS_HOSTNAME will be set to the system's hostname.
        :type interface: str
        :param user: Unprivileged user to launch the job as. Defaults to the user
            creating the job.
        :type user: str
        :param workspace_setup: Location of the workspace setup file to source for
            the job's ROS context. Defaults to the current workspace.
        :type workspace_setup: str
        :param rosdistro: rosdistro to use for the /etc/ros/DISTRO path. Defaults
            to $ROS_DISTRO from the current environment.
        :type rosdistro: str
        :param master_uri: For systems with multiple computers, you may want this
            job to launch with ROS_MASTER_URI pointing to another machine.
        :type master_uri: str
        :param log_path: The location to set ROS_LOG_DIR to. If changed from the
            default of using /tmp, it is the user's responsibility to manage log
            rotation.
        :type log_path: str
        """

        self.name = name

        self.interface = interface

        # Fall back on current user as the user to run ROS as.
        self.user = user or getpass.getuser()

        # Fall back on current workspace setup file if not explicitly specified.
        self.workspace_setup = workspace_setup or \
            os.environ['CMAKE_PREFIX_PATH'].split(':')[0] + '/setup.bash'

        # Fall back on current distro if not otherwise specified.
        self.rosdistro = rosdistro or os.environ['ROS_DISTRO']

        self.master_uri = master_uri or "http://127.0.0.1:11311"

        self.log_path = log_path or "/tmp"

        # Override this to false if you want to bypass generating the
        # upstart conf file.
        self.generate_system_files = True

        # Override this to True if you want to create symbolic link for
        # job launch files instead of copying them.
        self.symlink = False

        # Override this to True is you want the --wait flag passed to roslaunch.
        # This will be desired if the nodes spawned by this job are intended to
        # connect to an existing master.
        self.roslaunch_wait = False

        # Set of files to be installed for the job. This is only launchers
        # and other user-specified configs--- nothing related to the system
        # startup job itself. List of strs.
        self.files = []

        # Override this to True if the startup script should enter an endless
        # loop until getifip returns an IP address that is valid for ROS_IP
        # parameter.
        self.interface_loop = False

    def add(self, package=None, filename=None, glob=None):
        """ Add launch or other configuration files to Job.

        Files may be specified using relative, absolute, or package-relative
        paths. Files may also be specified using shell globs.

        :param package: Optionally specify a package to search for the file
            or glob relative-to.
        :type package: str
        :param filename: Name of a file to add to the job. Relative to the
            package path, if specified.
        :type filename: str
        :param glob: Shell glob of files to add to the job. Relative to the
            package path, if specified.
        :type glob: str
        """

        if package:
            search_paths = reversed(find_in_workspaces(project=package))
        else:
            search_paths = ('.', )

        if glob and filename:
            raise RuntimeError("You must specify only an exact filename or a glob, not both.")

        # See: https://docs.python.org/2/library/os.html#os.getlogin
        if filename:
            for path in search_paths:
                candidate = os.path.join(path, filename)
                if os.path.isfile(candidate):
                    self.files.append(candidate)

        if glob:
            for path in search_paths:
                self.files.extend(glob_files(os.path.join(path, glob)))

    def install(self, root="/", sudo="/usr/bin/sudo", Provider=None):
        """ Install the job definition to the system.

        :param root: Override the root to install to, useful for testing.
        :type root: str
        :param sudo: Override which sudo is used, useful for testing or for making
            it use gksudo instead.
        :type sudo: str
        :param provider: Override to use your own generator function for the system
            file preparation.
        :type provider: Provider
        """
        # This is a recipe of files and their contents which is pickled up and
        # passed to a sudo process so that it can create the actual files,
        # without needing a ROS workspace or any other environmental setup.
        if Provider is None:
            Provider = providers.detect_provider()
        p = Provider(root, self)
        installation_files = p.generate_install()

        print "Preparing to install files to the following paths:"
        for filename in sorted(installation_files.keys()):
            print "  %s" % filename

        self._call_mutate(sudo, installation_files)
        p.post_install()

    def uninstall(self, root="/", sudo="/usr/bin/sudo", Provider=None):
        """ Uninstall the job definition from the system.

        :param root: Override the root to uninstall from, useful for testing.
        :type root: str
        :param sudo: Override which sudo is used, useful for testing or for making
            it use gksudo instead.
        :type sudo: str
        :param provider: Override to use your own generator function for the system
            file preparation.
        :type provider: Provider
        """
        if Provider is None:
            Provider = providers.detect_provider()
        p = Provider(root, self)
        installation_files = p.generate_uninstall()

        if len(installation_files) == 0:
            print "Job not found, nothing to remove."
        else:
            print "Preparing to remove the following paths:"
            for filename in sorted(installation_files.keys()):
                print "  %s" % filename

            self._call_mutate(sudo, installation_files)

    def _call_mutate(self, sudo, installation_files):
        try:
            # Installed script location
            mutate_files_exec = find_in_workspaces(
                project="robot_upstart", path="mutate_files", first_match_only=True)[0]
        except IndexError:
            # Devel script location
            mutate_files_exec = find_in_workspaces(
                project="robot_upstart", path="scripts/mutate_files", first_match_only=True)[0]

        # If sudo is specified, then the user will be prompted at this point.
        cmd = [mutate_files_exec]
        if sudo:
            cmd.insert(0, sudo)
        print "Now calling: %s" % ' '.join(cmd)
        p = subprocess.Popen(cmd + [pickle.dumps(installation_files)])
        p.communicate()

        if p.returncode == 0:
            print "Filesystem operation succeeded."
        else:
            print "Error encountered; filesystem operation aborted."

        return p.returncode
