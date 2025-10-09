from setuptools import setup

package_name = 'dua_node_py'

setup(
    name=package_name,
    version='1.0.3',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name, ['dua_node_py/dua_node.py'])
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='dotX Automation s.r.l.',
    maintainer_email='info@dotxautomation.com',
    description='ROS 2 node base classes with DUA extensions.',
    license='Apache-2.0',
    tests_require=['pytest']
)
