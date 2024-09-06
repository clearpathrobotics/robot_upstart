import os
from setuptools import setup
from glob import glob

PACKAGE_NAME = 'robot_upstart'

setup(
    name=PACKAGE_NAME,
    version='1.0.3',
    packages=[PACKAGE_NAME],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + PACKAGE_NAME]),
        ('share/' + PACKAGE_NAME, ['package.xml']),
        (os.path.join('lib', PACKAGE_NAME, 'scripts'), glob('scripts/*')),
        (os.path.join('share', PACKAGE_NAME, 'scripts'), glob('scripts/*')),
        (os.path.join('share', PACKAGE_NAME, 'templates'), glob('templates/*')),
        (os.path.join('share', PACKAGE_NAME, 'test'), glob('test/*.py')),
        (os.path.join('share', PACKAGE_NAME, 'test/launch'), glob('test/launch/*.launch')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Tony Baltovski',
    maintainer_email='tbaltovski@clearpathrobotics.com',
    description='The robot_upstart package provides scripts which may be used to install and uninstall Ubuntu Linux upstart jobs which launch groups of roslaunch files.',
    license='BSD',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)
