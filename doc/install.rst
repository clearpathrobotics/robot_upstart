The ``install`` script
======================

.. argparse::
    :module: robot_upstart.install_script
    :func: get_argument_parser
    :prog: install


Permissions
-----------

It's important to understand how permissions work robot_upstart:

1. The upstart job invokes its `jobname-start` bash script as root.

2. The script sets up environment variables, and then uses setuidgid_ to execute roslaunch as an unprivileged user. This is by default the user who ran the install script, but it can also be specified explicitly via a flag.

3. The `roslaunch` which executes *does not have its user's group memberships*. This means that it will not have access to serial ports with the `dialout` group, or locations in `/var/log` owned by root, etc. Any filesystem resources needed by your ROS nodes should be chowned to the same unprivileged user which will run ROS, or should set to world readable/writeable, for example using udev. 

.. _setuidgid: http://manpages.ubuntu.com/manpages/trusty/man8/setuidgid.8.html 

Implementation
--------------

If you're in the process of transitioning from using the ``install`` script
to the Python API, it may be helpful to inspect exactly how the script uses
the API. You can find its implementation in the
:func:`robot_upstart.install_script.main` function.

.. automodule:: robot_upstart.install_script
    :members:
