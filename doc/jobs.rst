Jobs
====

.. automodule:: robot_upstart.job
    :members:

Example
-------

A minimal example of creating an upstart job using this API:

.. code-block:: py

    import robot_upstart

    j = robot_upstart.Job()
    j.add(package="myrobot_bringup", filename="launch/base.launch")
    j.install()

The :meth:`Job.add` method may be called multiple times, of course, and
you may alternatively specify a glob, if you're like to create a job which
launches all of the launchfiles from a package, eg:

.. code-block:: py

    import robot_upstart

    j = robot_upstart.Job()
    j.add(package="myrobot_bringup", glob="launch/*.launch")
    j.install()

Finally, if the ``package`` parameter is not specified, then the glob or
filename is relative to the current directory, rather than a package.
