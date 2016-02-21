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
import shutil

import spur

class WebserverExecutor(object):

  class Error(Exception): pass
  class RemoteExecutionError(Error): pass

  def __init__(self):
    self._username = None
    self._password = None
    self.username_path = os.path.join(os.getcwd(), "username")
    self.password_path = os.path.join(os.getcwd(), "password")

  @property
  def username(self):
    if self._username is None:
      with open(self.username_path, 'r') as fp:
        self._username = fp.read().strip()
    return self._username

  @property
  def password(self):
    if self._password is None:
      with open(self.password_path, 'r') as fp:
        self._password = fp.read().strip()
    return self._password

  def remote_command(self, hostname, command_list):
    shell = spur.SshShell(hostname=hostname, username=self.username, password=self.password,
        missing_host_key=spur.ssh.MissingHostKey.warn)
    result = None
    with shell:
      result = shell.run(command_list, allow_error=True)
    if result is not None:
      if result.return_code is not 0:
        raise self.RemoteExecutionError("Error code %d when connecting to %s: %s" % (
            result.return_code, hostname, result.stderr_output))
      return result.output
    raise self.RemoteExecutionError('Did not successfully run on %s!' % hostname)

  def create_staging_directory(self, hostname, path):
    return self.remote_command(hostname, ['mkdir', '-p', path])

  def update_packages(self, hostname):
    return self.remote_command(hostname, ['apt-get', 'update'])

  def install_packages(self, hostname, packages):
    """Ensure a given sent of deb packages are installed on a host.

    This will raise RemoteExecutionError to bubble up problems

    :param hostname: Server to execute on
    :type hostname: str
    :param packages: tuple of a package name to install, followed by an optional command to execute
    :type packages: (str, []) or (str, None)
    """
    for package, post_install_command in packages:
      print('Installing %s on %s' % (package, hostname))
      output = self.remote_command(hostname, ['apt-get', '-y', 'install', package])
      print('Output: %s' % output)

      if 'is already the newest version' not in output and post_install_command:
        print('Modifying %s with: %s' % (hostname, post_install_command))
        output = self.remote_command(hostname, post_install_command)
        print('Output: %s' % output)

  def stage_artifact(hostname, local_path, artifact_version, staging_dir):
    connection = spur.SshShell(hostname=hostname, username=self.username, password=self.password,
        missing_host_key=spur.ssh.MissingHostKey.warn)
    remote_artifact = os.path.join(staging_dir, local_path)
    with connection.open(remote_artifact, 'wb') as remote_file:
      with open(local_path, 'rb') as local_file:
        shutil.copyfileobj(local_file, remote_file)
    self.remote_command(hostname, ['unzip', '-d', os.path.join(staging_dir, artifact_version), remote_artifact])
    #self.remote_command(hostname, ['rm', remote_artifact])


  def application_version(self, hostname):
    return self.remote_command(hostname, ['uname', '-a'])
