#!/usr/bin/env python
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

import argparse
import os

import robot_upstart
from catkin.find_in_workspaces import find_in_workspaces

import providers

DESC_PKGPATH = ("Make sure the path starts with the package name"
                " (e.g. don't pass absolute path nor a path starting from"
                " workspace top folder etc.)")


def get_argument_parser():
    p = argparse.ArgumentParser(
        description="""Use this tool to quickly and easily create system startup jobs which run one or more
        ROS launch files as a daemonized background process on your computer. More advanced users will prefer
        to access the Python API from their own setup scripts, but this exists as a simple helper, an example,
        and a compatibility shim for previous versions of robot_upstart which were bash-based.""")

    p.add_argument("pkgpath", type=str, nargs='+', metavar="pkg/path",
                   help="Package and path to install job launch files from. " +
                        DESC_PKGPATH)
    p.add_argument("--job", type=str,
                   help="Specify job name. If unspecified, will be constructed from package name.")
    p.add_argument("--interface", type=str, metavar="ethN",
                   help="Specify network interface name to associate job with.")
    p.add_argument("--user", type=str, metavar="NAME",
                   help="Specify user to launch job as.")
    p.add_argument("--setup", type=str, metavar="path/to/setup.bash",
                   help="Specify workspace setup file for the job launch context.")
    p.add_argument("--rosdistro", type=str, metavar="DISTRO",
                   help="Specify ROS distro this is for.")
    p.add_argument("--master", type=str, metavar="http://MASTER:11311",
                   help="Specify an alternative ROS_MASTER_URI for the job launch context.")
    p.add_argument("--logdir", type=str, metavar="path/to/logs",
                   help="Specify an a value for ROS_LOG_DIR in the job launch context.")
    p.add_argument("--augment", action='store_true',
                   help="Bypass creating the job, and only copy user files. Assumes the job was previously created.")
    p.add_argument("--provider", type=str, metavar="[upstart|systemd]",
                   help="Specify provider if the autodetect fails to identify the correct provider")
    p.add_argument("--symlink", action='store_true',
                   help="Create symbolic link to job launch files instead of copying them.")
    p.add_argument("--interface_loop", action='store_true',
                   help="Wait in an endless loop for getifip to return a valid IP address.")
    return p


def main():
    """ Implementation of the ``install`` script."""

    args = get_argument_parser().parse_args()

    pkg, pkgpath = args.pkgpath[0].split('/', 1)
    job_name = args.job or pkg.split('_', 1)[0]

    # Any unspecified arguments are on the args object as None. These are filled
    # in by the Job constructor when passed as Nones.
    j = robot_upstart.Job(
        name=job_name, interface=args.interface, user=args.user,
        workspace_setup=args.setup, rosdistro=args.rosdistro,
        master_uri=args.master, log_path=args.logdir)

    for this_pkgpath in args.pkgpath:
        pkg, pkgpath = this_pkgpath.split('/', 1)
        if not pkg:
            print("Unable to locate package your job launch is in."
                  " Installation aborted. " + DESC_PKGPATH +
                  "\npkgpath passed: {}.".format(pkgpath))
            return 1

        found_path = find_in_workspaces(project=pkg, path=pkgpath, first_match_only=True)
        if not found_path:
            print "Unable to locate path %s in package %s. Installation aborted." % (pkgpath, pkg)
            return 1

        if os.path.isfile(found_path[0]):
            # Single file, install just that.
            j.add(package=pkg, filename=pkgpath)
        else:
            # Directory found, install everything within.
            j.add(package=pkg, glob=os.path.join(pkgpath, "*"))

    if args.augment:
        j.generate_system_files = False
    if args.interface_loop:
        j.interface_loop = True

    provider = providers.detect_provider()
    if args.provider == 'upstart':
        provider = providers.Upstart
    if args.provider == 'systemd':
        provider = providers.Systemd
    if args.symlink:
        j.symlink = True

    j.install(Provider=provider)

    return 0
