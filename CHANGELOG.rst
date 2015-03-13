^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package robot_upstart
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

0.0.7 (2015-03-13)
------------------
* if logdir does not exist, try to create it, if this fails, fall back to /tmp
* fix invalid range error on grep
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
