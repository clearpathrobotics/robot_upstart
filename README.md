robot_upstart
=============

Clearpath Robotics presents a suite of scripts to assist with launching background ROS processes on Ubuntu Linux PCs.


Motivation
----------

The intention is to standardize the upstart portion which has traditionally been included in <robot>_bringup packages. Functionality includes:

* Install an upstart job to run upon the availability of a network interface.
* Copy launch files from package to /etc/ros/<distro>/<job>.d/
* Upon job start, coalesce launch files (mklaunch) and launch them together.

Usage
-----

To install a job from the command line, it can be as simple as:

    rosrun robot_upstart install turtlebot_bringup/launch/minimal.launch --interface wlan0

This will create a job called turtlebot, which comes up with the wireless. Alternatively, you can manually start and stop the job like so:

    sudo service turtlebot start
    sudo service turtlebot stop

For robots with many components, the job can also glob a whole directory of launch files into a single roslaunch instance. For example:

    rosrun robot_upstart install husky_bringup/launch/core

This copies all the launch files from the folder into /etc/ros/hydro/husky.d. At launch time, a /tmp/husky.launch file will be created which <include>s the launch files from this folder.

For debugging reasons, you can also foreground launch it by running the start script directly:

    sudo husky-start

This will show the console output, any errors, and the result of the final roslaunch.

For Platform Maintainers
------------------------

If you maintain the ROS software for a common platform, you can take advantage of upstart and still provide a seamless installation process for users. For example, in your myplatform_bringup package, maintain a directory of launch files which represent the platform's set of bootstrap ROS nodes, and then in a scripts directory, add an install file which calls through to robot_upstart, eg:

    #!/bin/bash
    rosrun robot_upstart install myplatform_bringup/launch
    # Other platform setup (udev rules, network config, etc)

Now a user can add the platform software packages and it's a one-liner to be fully set up:

    rosrun myplatform_bringup install
