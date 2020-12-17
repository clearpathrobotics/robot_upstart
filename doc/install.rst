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

2. The script sets up environment variables, and then uses setpriv_ to execute roslaunch as an unprivileged user. This is by default the user who ran the install script, but it can also be specified explicitly via a flag.

3. The `roslaunch` which executes preserves its user's group memberships.  This means that the user should be configured to be a member of any applicable groups required by the ROS nodes being launched.  This will commonly include the `dialout` and `plugdev` groups for serial devices, and `audio` for speakers and microphones.  Any filesystem resources needed by your ROS nodes should be chowned and chmodded to be accessible to the same unprivileged user which will run ROS.

.. _setpriv: https://man7.org/linux/man-pages/man1/setpriv.1.html

Implementation
--------------

If you're in the process of transitioning from using the ``install`` script
to the Python API, it may be helpful to inspect exactly how the script uses
the API. You can find its implementation in the
:func:`robot_upstart.install_script.main` function.

.. automodule:: robot_upstart.install_script
    :members:
