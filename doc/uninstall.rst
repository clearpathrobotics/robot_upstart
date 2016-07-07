The ``uninstall`` script
========================

.. argparse::
    :module: robot_upstart.uninstall_script
    :func: get_argument_parser
    :prog: uninstall

Caveats
-------

The uninstall script (and underlying method) make few guarantees--- all that ``uinstall`` will do
is attempt to remove the files which were recorded as created by the last-run ``install`` action.
It's not able to remove files added manually to a job after installation, nor can it detect and
warn about modifications made to files.

If the installed files are moved or the ``.installed_files`` manifest file is not intact,
uninstallation will fail.


Implementation
--------------

You can find this script's implementation in the
:func:`robot_upstart.uninstall_script.main` function.

.. automodule:: robot_upstart.uninstall_script
    :members:
