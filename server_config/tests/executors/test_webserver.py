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

import unittest

from server_config.executors.webserver import WebserverExecutor

import mock
from nose.tools import assert_equals
from spur.results import ExecutionResult


HOSTNAME = 'hostA'


class TestWebserverExecutor(unittest.TestCase):
  def setUp(self):
    self.executor = WebserverExecutor()

  @mock.patch('spur.SshShell.run', autospec=True, spec_set=True)
  def test_remote_command(self, mock_run):
    mock_run.return_value = ExecutionResult(0, 'stdout', 'stderr')
    assert_equals(self.executor.remote_command(HOSTNAME, ['test']), 'stdout')

  @mock.patch('spur.SshShell.run', autospec=True, spec_set=True)
  def test_remote_command_failed_command(self, mock_run):
    mock_run.return_value = ExecutionResult(1, 'stdout', 'stderr')
    with self.assertRaises(self.executor.RemoteExecutionError):
      self.executor.remote_command(HOSTNAME, ['test'])

  @mock.patch('server_config.executors.webserver.WebserverExecutor.remote_command', autospec=True,
      spec_set=True)
  def test_create_directory(self, mock_remote_command):
    mock_remote_command.return_value = 'test_output'
    assert_equals(self.executor.create_directory(HOSTNAME, 'path'), 'test_output')
    assert_equals(mock_remote_command.mock_calls,
        [mock.call(self.executor, HOSTNAME, ['mkdir', '-p', 'path'])])

  @mock.patch('server_config.executors.webserver.WebserverExecutor.remote_command', autospec=True,
      spec_set=True)
  def test_update_packages(self, mock_remote_command):
    mock_remote_command.return_value = 'test_output'
    assert_equals(self.executor.update_packages(HOSTNAME), 'test_output')
    assert_equals(mock_remote_command.mock_calls,
        [mock.call(self.executor, HOSTNAME, ['apt-get', 'update'])])