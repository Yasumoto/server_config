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


# command should zip up the current hello_world directory, include the git sha in the filename
# for each file, ssh into the host
# if apache2, php5, or libapche2-mod-php5 are not present
  # sudo apt-get install apache2 php5 libapache2-mod-php5
  # sudo /etc/init.d/apache2 restart
  # rm index.html (for apache2 only)
# scp over the new zip file to a staging directory that you create
# unzip it into /var/www/html
# urllib.urlopen(), ensure Hello, World! (make a comment that it can change)

from contextlib import contextmanager
import os

from server_config.operator import Operator

class WebserverOperator(Operator):
  @property
  def name(self):
    return 'webserver'

  @contextmanager
  def hostlist(self):
    with open(os.path.join(os.getcwd(), '%s.txt' % self.name), 'r') as hostlist:
      yield hostlist.read().strip().split('\n')

  def preflight_check(self):
    pass

  def status(self, hostname):
    pass

  def deploy(self, hostname, version):
    pass
