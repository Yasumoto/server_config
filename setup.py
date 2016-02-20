# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
from setuptools import find_packages, setup
import sys


HERE = os.path.abspath(os.path.dirname(__file__))


def readme():
    with open(os.path.join(HERE, 'README.rst')) as f:
        return f.read()


setup(name='server_config',
      version='0.0.2',
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
        'console_scripts': ['server-config=server_config.command_line:main'],
      },
      install_requires=[
        'click==6.2',
      ],
      test_suite='nose.collector',
      tests_require=[
        'mock==1.3.0',
        'nose==1.3.7'
      ],
      include_package_data=True,
      zip_safe=True)
