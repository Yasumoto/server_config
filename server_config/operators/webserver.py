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
import subprocess
import time
import urllib2

from server_config.executors.webserver import WebserverExecutor
from server_config.operator import Operator

import arrow

class WebserverOperator(Operator):
  """Overall manager to maintain consistency between Webserver hosts"""

  PACKAGE_LIST = (
    ('apache2=2.4.7-1ubuntu4.9', ['rm', '-f', '/var/www/html/index.html']),
    ('php5=5.5.9+dfsg-1ubuntu4.14', None),
    ('libapache2-mod-php5=5.5.9+dfsg-1ubuntu4.14', ['/etc/init.d/apache2', 'restart']),
  )

  SYMLINK_LOCATION = '/var/www/html'
  HEALTH_CHECK = 'Hello, world!'

  def __init__(self):
    self._executor = None
    self.staging_dir = os.path.join(self.STAGING_DIRECTORY, self.name)

  @property
  def name(self):
    return 'webserver'

  @property
  def executor(self):
    if self._executor is None:
      self._executor = WebserverExecutor()
    return self._executor

  @contextmanager
  def hostlist(self):
    with open(os.path.join(os.getcwd(), '%s.txt' % self.name), 'r') as hostlist:
      yield hostlist.read().strip().split('\n')

  def preflight_check(self):
    """Run through steps required to support the application before deployment."""
    with self.hostlist() as hostnames:
      for hostname in hostnames:
        self.executor.create_directory(hostname, self.staging_dir)
        self.executor.install_packages(hostname, self.PACKAGE_LIST)

  def status(self):
    """Return the currently deployed version on each server."""
    application_versions = {}
    with self.hostlist() as hostnames:
      for hostname in hostnames:
        try:
          application_versions[hostname] = self.executor.application_version(hostname,
              self.SYMLINK_LOCATION)
        except WebserverExecutor.RemoteExecutionError as e:
          print('Error connecting to %s: %s' % (hostname, e))
        print('%s had %s' % (hostname, application_versions[hostname]))
    return application_versions

  def build_artifact(self):
    """Simple build process for hello_world.

    Future improvements would likely benefit from more process- likely splitting the larger codebase
    into a separate repository, running tests ahead of time, and committing a built artifact to
    something like artifactory.
    """
    artifact_version = arrow.utcnow().timestamp
    local_path = 'hello_world_%s.tar.gz' % artifact_version
    subprocess.check_call(['/usr/bin/tar', '-czf', local_path, 'hello_world'])
    return local_path, artifact_version

  def deploy(self, clock=time):
    """Install a new version of the hello_world web application.
    
    :param clock: Specified to make testing easier and more explicit
    """
    local_path, artifact_version = self.build_artifact()

    with self.hostlist() as hostnames:
      for hostname in hostnames:
        old_version = self.executor.application_version(hostname, self.SYMLINK_LOCATION)
        self.executor.stage_artifact(hostname, local_path, artifact_version, self.staging_dir)
        self.executor.set_version(hostname, artifact_version, self.staging_dir,
            self.SYMLINK_LOCATION)
        clock.sleep(5)
        page = urllib2.urlopen('http://%s' % hostname, 'r').read()
        print('New Deploy Contents: %s' % page)
        if self.HEALTH_CHECK not in page:
          print('ERROR! %s did not deploy %s successfully! Rolling back to %s and halting.' % (
              hostname, artifact_version, old_version))
          self.executor.set_version(hostname, old_version, self.staging_dir,
              self.SYMLINK_LOCATION)
          return False
        print('%s is successful!' % hostname)
        
