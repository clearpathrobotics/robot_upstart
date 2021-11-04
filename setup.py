import os
from setuptools import setup
from glob import glob

package_name = 'robot_upstart'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('lib', package_name, 'scripts'), glob('scripts/*')),
        (os.path.join('share', package_name, 'scripts'), glob('scripts/*')),
        (os.path.join('share', package_name, 'templates'), glob('templates/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='fengqi',
    maintainer_email='zifengqi123@sina.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)
