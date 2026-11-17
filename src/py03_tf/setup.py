from setuptools import find_packages, setup

package_name = 'py03_tf'

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
            'demo01_static_tf_broadcaster_py = py03_tf.demo01_static_tf_broadcaster_py:main',
            'demo02_dynamic_tf_broadcaster_py = py03_tf.demo02_dynamic_tf_broadcaster_py:main',
            'demo03_tf_point_broadcaster_py = py03_tf.demo03_tf_point_broadcaster_py:main',
            'demo04_tf_listener_py = py03_tf.demo04_tf_listener_py:main'

        ],
    },
)
