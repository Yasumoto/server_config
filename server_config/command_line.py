#!/usr/bin/env python
#
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

# check argument
# do we have a hostlist with that name
# if so, delegate to that command
# command should zip up the current hello_world directory, include the git sha in the filename
# for each file, ssh into the host
# if apache2, php5, or libapche2-mod-php5 are not present
  # sudo apt-get install apache2 php5 libapache2-mod-php5
  # sudo /etc/init.d/apache2 restart
  # rm index.html (for apache2 only)
# scp over the new zip file to a staging directory that you create
# unzip it into /var/www/html
# urllib.urlopen(), ensure Hello, World! (make a comment that it can change)

import click

@click.command()
@click.option('--role', default='', help='Servers to operate upon')
@click.option('--action', default='list', help='Action to perform, currently `list` or `deploy`')
def main(role, action):
  """Tool used to perform actions upon hosts in production."""
  