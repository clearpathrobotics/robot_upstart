^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package robot_upstart
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Forthcoming
-----------
* Using setpriv (`#101 <https://github.com/clearpathrobotics/robot_upstart/issues/101>`_)
  * Try replacing setuidgid with setpriv to see if this is a viable solution to the group permission issues
  * Fix a typo
  * Set the real and effective user and group IDs, not just the real ones
  * Add a missing "roslaunch" argument to the actual launch. Whoops :/
* Contributors: Chris I-B

0.3.1 (2021-03-01)
------------------
* [doc] Add commands when systemd is chosen. (`#78 <https://github.com/clearpathrobotics/robot_upstart/issues/78>`_)
  When `systemd` is specified as a provider, commands are different.
  https://wiki.ubuntu.com/SystemdForUpstartUsers
  [doc] Add systemd start/stop commands.
* Melodic compatibility: modify getifip for bionic output (`#88 <https://github.com/clearpathrobotics/robot_upstart/issues/88>`_)
  * Add net-tools as dependency because ifconfig is used
  * Modify getifip to handle bionic ifconfig output
* Break line that the linter doesn't like. (`#87 <https://github.com/clearpathrobotics/robot_upstart/issues/87>`_)
* [doc] Clarify the logic for automated job name determination. (`#82 <https://github.com/clearpathrobotics/robot_upstart/issues/82>`_)
  Problem addressed
  =================
  When `--job` option is not passed to `rosrun robot_upstart install`, the job name gets determined automatically but the logic of it is not clear.
  Solution to the problem
  =======================
  Add an explanation to the document.
* [CI][kinetic-devel] Update to Xenial. (`#79 <https://github.com/clearpathrobotics/robot_upstart/issues/79>`_)
  * [CI][kinetic-devel] Update to Xenial.
  On a PR https://github.com/clearpathrobotics/robot_upstart/pull/78 I saw [CI failure](https://travis-ci.org/clearpathrobotics/robot_upstart/builds/507510733?utm_source=github_status&utm_medium=notification) that seems to be related to platform issue. Using `trusty` for xenial-based job might not work (any more?).
  ```
  Unpacking python-rospkg (1.1.7-100) ...
  dpkg-deb: error: archive '/var/cache/apt/archives/python-rosdep_0.15.1-1_all.deb' has premature member 'control.tar.xz' before 'control.tar.gz', giving up
  dpkg: error processing archive /var/cache/apt/archives/python-rosdep_0.15.1-1_all.deb (--unpack):
  subprocess dpkg-deb --control returned error exit status 2
  No apport report written because MaxReports is reached already
  Processing triggers for man-db (2.6.7.1-1ubuntu1) ...
  Processing triggers for shared-mime-info (1.2-0ubuntu3) ...
  Processing triggers for sgml-base (1.26+nmu4ubuntu1) ...
  Errors were encountered while processing:
  /var/cache/apt/archives/python-catkin-pkg-modules_0.4.10-1_all.deb
  /var/cache/apt/archives/python-catkin-pkg_0.4.10-100_all.deb
  /var/cache/apt/archives/python-rosdistro-modules_0.7.2-1_all.deb
  /var/cache/apt/archives/python-rosdistro_0.7.2-100_all.deb
  /var/cache/apt/archives/python-rosdep_0.15.1-1_all.deb
  E: Sub-process /usr/bin/dpkg returned an error code (1)
  The command "sudo apt-get install python-rosdep -y" failed and exited with 100 during .
  ```
  * [CI] Switch to industrial_ci. Add ROS2 dashing.
  * [CI] Remove ROS2 dashing for now (see https://github.com/clearpathrobotics/robot_upstart/pull/79#issuecomment-533908848).
* Add support for wait flag in the install script (`#73 <https://github.com/clearpathrobotics/robot_upstart/issues/73>`_)
* Contributors: Isaac I.Y. Saito, Mateusz Sadowski, Mike Purvis, Ramon Wijnands

0.3.0 (2018-05-23)
------------------
* Add a dependency onto network-online.target (`#67 <https://github.com/clearpathrobotics/robot_upstart/issues/67>`_)
* Clarify the reason of the error due to wrong pkgpath passed. (`#57 <https://github.com/clearpathrobotics/robot_upstart/issues/57>`_)
* Allow ROS_HOME to be set previously by env file. (`#54 <https://github.com/clearpathrobotics/robot_upstart/issues/54>`_)
* Contributors: Isaac I.Y. Saito, Thomas Furfaro, mhosmar-cpr

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
