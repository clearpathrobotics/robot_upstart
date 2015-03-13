^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package robot_upstart
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Forthcoming
-----------
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
