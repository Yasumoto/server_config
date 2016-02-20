import os
from setuptools import find_packages, setup
import sys


HERE = os.path.abspath(os.path.dirname(__file__))


def readme():
    with open(os.path.join(HERE, 'README.rst')) as f:
        return f.read()


setup(name='server_config',
      version='0.0.1',
      description='A Simple Configuration Tool for Servers',
      long_description=readme(),
      classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: System :: Distributed Computing',
        'Topic :: System :: Systems Administration'
      ],
      keywords='Configuration Management',
      url='https://github.com/Yasumoto/server_config',
      author='Joe Smith',
      author_email='yasumoto7@gmail.com',
      license='Apache',
      packages=['server_config'],
      entry_points={
        'console_scripts': ['jimmeh=server_config.command_line:main'],
      },
      install_requires=[
        'click==6.2',
      ],
      test_suite='nose.collector',
      tests_require=['nose==1.3.7'],
      include_package_data=True,
      zip_safe=True)
