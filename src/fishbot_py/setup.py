from setuptools import find_packages, setup

package_name = 'fishbot_py'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='robot',
    maintainer_email='robot@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'initialpose_py = fishbot_py.initialpose_py:main',
            'dynamic_tf_listener = fishbot_py.dynamic_tf_listener:main',
            'navtopose_py = fishbot_py.navtopose_py:main',
            'waypoint_py = fishbot_py.waypoint_py:main',



        ],
    },
)
