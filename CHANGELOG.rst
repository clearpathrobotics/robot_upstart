^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package robot_upstart
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

0.2.2 (2017-01-23)
------------------
* Added a spin wait until ros processes exit. (`#40 <https://github.com/clearpathrobotics/robot_upstart/issues/40>`_)
* Moved detect_providers to providers.py (`#46 <https://github.com/clearpathrobotics/robot_upstart/issues/46>`_)
* Miscellaneous source code fixups.
* Contributors: Mike Purvis, Tony Baltovski, Zac Witte

0.2.1 (2016-12-19)
------------------
* Added option to install under systemd rather than upstart (`#41 <https://github.com/clearpathrobotics/robot_upstart/issues/41>`_)
* Added option to add launch files as symbolic link (`#43 <https://github.com/clearpathrobotics/robot_upstart/issues/43>`_)
* Fix title underline to silence doc job warning.
* Update README.md
  Use `latest_available` URL for documentation link.
* Merge pull request `#31 <https://github.com/clearpathrobotics/robot_upstart/issues/31>`_ from clearpathrobotics/roslint_fix
  Remove unwanted whitespace
* Remove unwanted whitespace
* Merge pull request `#28 <https://github.com/clearpathrobotics/robot_upstart/issues/28>`_ from clearpathrobotics/install_multiple_files
  Updated install script to allow adding multiple launch files to a job
* Ensure script aborts if one of the provided launch files cannot be found
* Updated install script to allow adding multiple launch files to a job at once
* Fix leftover {user} tokens in template.
* Formatting changes for new pep8.
* Contributors: Jonathan Jekir, Kazumi Malhan, Mike Purvis, Niklas Casaril

0.2.0 (2015-03-14)
------------------
* Linter fixes.
* Contributors: Mike Purvis

0.1.2 (2015-03-13)
------------------
* Add some basic install/uninstall tests.
* Add uninstall job method and script.
* Remove out of date README content, now forwards to ROS Wiki and generated documentation.
* Add a documentation section about permissions
* Contributors: Gaël Ecorchard, Mike Purvis

0.1.1 (2015-01-20)
------------------
* Python Rewrite
* The startup event is too early for ROS to start, use local-filesystems instead.
* Remove bash versions of the install and uninstall utilities.
* Add support for supplying the --wait flag to roslaunch.
* Add Sphinx documentation.
  To get the argparse docs required moving most of the install
  script to a module, which probably should have been done anyway.
* Add a new-implementation install script, refactor Provider to be a class rather than function.
* Add roslint.
* Initial implementation of Python job generator.
* Port templated files to use empy.
  This gets rid of the bespoke templating system that was so bad. Also
  notable here is adding a --root flag to install somewhere other than
  the actual root. This needs to be further fleshed out, for example
  by not reinvoking with sudo when installing to non-root location.
* use LANG=C for ifconfig
* add argument to specify log directory
* Contributors: Eisoku Kuroiwa, Mike Purvis, ipa-mig

0.0.6 (2014-02-25)
------------------
* Add capability to also generate amalgamated descriptions, similar to launch files.
* Update package.xml
* Contributors: Mike Purvis

0.0.5 (2013-09-13)
------------------
* Better console outputs.
* Remove debug output from install script.

0.0.4 (2013-09-11)
------------------
* Provide --augment option, to add files to a job without creating a new one.
* Explicitly depend on daemontools.

0.0.3 (2013-09-11)
------------------
* Supply ROS_HOME explicitly in start script.
* Remove spurious comment from uninstall script.

0.0.2 (2013-09-06)
------------------
* Eliminate rosrun from the make process.

0.0.1 (2013-09-06)
------------------
* Generalized robot upstart scripts based on turtlebot_bringup
* Includes install and uninstall scripts
