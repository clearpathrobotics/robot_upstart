# robot_upstart [![robot_upstart_ci](https://github.com/clearpathrobotics/robot_upstart/actions/workflows/ci.yml/badge.svg?branch=jazzy)](https://github.com/clearpathrobotics/robot_upstart/actions/workflows/ci.yml)

`robot_upstart` provides a suite of scripts and a Python API to install and uninstall Linux
startup jobs that launch groups of ROS 2 launch files when a machine boots. It detects the
available init system and creates a `systemd` service (default) or an `upstart` job for your
robot, so your bringup starts automatically and can be managed like any other system service.

## Installation

From the ROS 2 apt repository (recommended):

```bash
sudo apt install ros-$ROS_DISTRO-robot-upstart
```

From source, in a colcon workspace:

```bash
cd ~/ros2_ws/src
git clone https://github.com/clearpathrobotics/robot_upstart.git
cd ~/ros2_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

## Usage

Create a startup job from one or more launch files. The following creates a job named `myrobot`
(derived from the package name) that launches `base.launch.py`:

```bash
ros2 run robot_upstart install myrobot_bringup/launch/base.launch.py
```

The job starts automatically on the next boot. With `systemd` (the default) you can also manage it
manually:

```bash
sudo systemctl start myrobot
sudo systemctl stop myrobot
```

To inspect the job output:

```bash
sudo journalctl -u myrobot
```

To remove a previously installed job:

```bash
ros2 run robot_upstart uninstall myrobot
```

Common options for `install` include `--job` (job name), `--rmw` (RMW implementation),
`--ros_domain_id`, `--user`, `--setup` (workspace setup file), and `--rosdistro`. Run
`ros2 run robot_upstart install --help` for the full list.

### Python API

Jobs can also be created programmatically:

```python
import robot_upstart

j = robot_upstart.Job(name="myrobot", rosdistro="jazzy")
j.add(package="myrobot_bringup", filename="launch/base.launch.py")
j.install()
```

## Documentation

Additional documentation is maintained in the [`doc/`](doc) directory of this repository.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup, linting, and pull request guidelines.

## License

`robot_upstart` is released under the [BSD license](LICENSE).
