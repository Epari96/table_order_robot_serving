from setuptools import find_packages, setup

package_name = 'table_order'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/resource', ['resource/TableOrder.ui']),
        ('share/' + package_name + '/resource',
        ['resource/짜장면.jpg',
         'resource/짬뽕.jpg',
         'resource/탕수육.jpg',
         'resource/제로 콜라.jpg']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='root',
    maintainer_email='root@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'table_gui = table_order.table_order:main'
        ],
    },
)
