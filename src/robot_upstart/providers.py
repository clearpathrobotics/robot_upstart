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
These functions implement the translation from user-intended behaviours
as specified in the state of the Job class to the system-specific configuration
files. At present, there is only an upstart configuration, but similar providers
could be defined for systemd, supervisor, launchd, or other systems.
"""

import em
import os
import StringIO

from catkin.find_in_workspaces import find_in_workspaces


def upstart(root, job):
    job.job_path = os.path.join(root, "etc/ros", job.rosdistro, job.name + ".d")

    # Make up list of files to copy to system locations.
    installation_files = {}
    for filename in job.files:
        with open(filename) as f:
            dest_filename = os.path.join(job.job_path, os.path.basename(filename))
            installation_files[dest_filename] = {"content": f.read()}

    # Share a single instance of the empy interpreter. Because it is outputting
    # to a StringIO, that object needs to be truncated between templates.
    output = StringIO.StringIO()
    interpreter = em.Interpreter(output=output, globals=job.__dict__.copy())

    def do_template(template, output_file, chmod=644):
        with open(find_in_workspaces(project="robot_upstart", path=template)[0]) as f:
            interpreter.file(f)
            installation_files[output_file] = {"content": output.getvalue(), "chmod": chmod}
            output.truncate(0)

    do_template("templates/job.conf.em", os.path.join(root, "etc/init", job.name + ".conf"), 755)
    do_template("templates/job-start.em", os.path.join(root, "usr/sbin", job.name + "-start"), 755)
    do_template("templates/job-stop.em", os.path.join(root, "usr/sbin", job.name + "-stop"))
    interpreter.shutdown()

    return installation_files
