Upstart for ROS Robots
======================

This package aims to assist with creating simple platform-specific jobs
to start your robot's ROS 2 launch files when its PC powers up.

.. toctree::
    :hidden:

    install
    uninstall
    jobs
    providers


Usage
-----

The basic or one-off usage is with the ``install`` script, which can be
as simple as:

.. code-block:: bash

    $ ros2 run robot_upstart install myrobot_bringup/launch/base.launch.py

This will create a job called ``myrobot`` on your machine, which launches
base.launch.py. It will start automatically when you next start your machine,
or you can bring it up and down manually (command may differ per providers (``systemd`` by default)):

.. code-block:: bash

    When systemd is in use
    $ sudo systemctl start myrobot
    $ sudo systemctl stop myrobot

    When upstart is in use
    $ sudo service myrobot start
    $ sudo service myrobot stop

If the job is crashing on startup, or you otherwise want to see what is
being output to the terminal on startup, check the log:

.. code-block:: bash

    systemd
    $ sudo journalctl -u myrobot


    upstart
    $ sudo tail /var/log/upstart/myrobot.log -n 30

For more details, please see :doc:`install` and :doc:`uninstall`.


Python API
----------

More advanced users or platform maintainers will prefer to script the
job creation as part of a larger installation script which may do other
tasks, such as pick and choose which launchers to install based on a
recipe, interactive wizard, or hardware introspection scheme.

These users will want to work with the Python API, which is detailed 
in :doc:`jobs`.


Extending
---------

If you're interesting in adding support for other init schemes to
robot_upstart, please see :doc:`providers`.


Index
-----

* :ref:`genindex`
* :ref:`search`
