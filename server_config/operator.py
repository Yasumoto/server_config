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

import abc

class Error(Exception):
  """Generic error received when operating on hosts."""
  pass


class Operator(object):
  """
  Abstract class which defines the interface for expected operations on each class of server.

  It is expected that each new type of server added to the cluster will have a corresponding
  Operator defined, and it is expected that most if not all functions are defined and tailored to
  support that specific role's operations and procedures.

  Future operations could be along the lines of 'send for repair', 'reboot', 'reimage', 'kernel
  upgrade', etc.
  """
  __metaclass__ = abc.ABCMeta

  STAGING_DIRECTORY = '/usr/local/server_config'

  @abc.abstractproperty
  def name(self):
    """The name of this operator, the same as the role of hosts.

    :rtype: str
    """
    pass

  @abc.abstractproperty
  def executor(self):
    """"Execution engine that will provide methods to connect to hosts and perform remote actions.

    :rtype: server_config.executor.Executor
    """
    pass

  @abc.abstractmethod
  def hostlist(self):
    """Open a file with the Operator name and yield it for reading.

    Implementations are expected to be a contextmanager for simplicity, along the lines of:

      @contextmanager
      def hostlist(self):
        with open(os.path.join(os.getcwd(), '%s.txt' % self.name), 'r') as hostlist:
          yield hostlist.read().strip().split('\n')

    And callers can use it as:

      for hostname in self.hostlist():
        print(hostname)


    This is kept abstract as certain environments may aim to keep host lists in a single source of
    truth, such as svn, a remote webserver, or a mounted NFS share.
    """
    pass

  @abc.abstractmethod
  def preflight_check(self):
    """An opportunity to ensure either the environment, configuration, or other setup is ready."""
    pass

  @abc.abstractmethod
  def status(self, hostname):
    """Connect and determine the state of a server by returning installed configuration version

    Note that failures can throw subclasses of the Error class in this module.

    :param hostname: The server to connect to and list its status
    :type hostname: str
    :rtype: string denoting the version deployed to the server
    """
    pass

  @abc.abstractmethod
  def deploy(self, hostname, version):
    """Connect to a host and apply the specified version of configuration to it.

    Note that failures can throw subclasses of the Error class in this module.

    :param hostname: Server name to connect to and operate upon
    :type hostname: str
    :param version: String matching the git tag to deploy
    :type version: str
    :rtype: bool indicating success or failure
    """
    pass
