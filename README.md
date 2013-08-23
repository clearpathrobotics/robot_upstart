upstart
=======

Clearpath Robotics presents a suite of scripts to assist with launching background ROS processes on Ubuntu Linux PCs.


Motivation
----------

The intention is to standardize the upstart portion which has traditionally been included in <robot>\_bringup packages. Functionality includes:

* Install an upstart job to run upon the availability of a network interface.
* Copy launch files from package to /etc/ros/<distro>/<job>.d/
* Upon job start, coalesce launch files (mklaunch) and launch them together.

Usage
-----

To install a job from the command line, it can be as simple as:

    rosrun upstart install --launch-dir myrobot\_bringup/launch --interface wlan0

This will create a job called myrobot, which comes up with the wireless. Alternatively, you can manually start the job like so:

    sudo service myrobot start

At this point, a /tmp/myrobot.launch file will be created which <include>s in the launch files from /etc which were copied there in the install step. This generated launch file is roslaunched as your own user, in the background.

If it doesn't start up, you can foreground launch it by running the start script directly:

    sudo myrobot-start

This will show the console output, any errors, and the result of the final roslaunch.
