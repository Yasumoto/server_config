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


HOSTNAME = 'hostA'


class TestWebserverExecutor(unittest.TestCase):
  def setUp(self):
    self.executor = WebserverExecutor()

  @mock.patch('subprocess.Popen', autospec=True, spec_set=True)
  def test_remote_command(self, MockPopen):
    return True
    MockPopen.return_value.communicate.return_value = 'success', ''

    assert_equals(self.executor.remote_command(HOSTNAME, ['test']), ('success', ''))

    assert_equals(MockPopen.mock_calls,
        [mock.call([self.executor.ssh_path, HOSTNAME, 'test'], stderr=-1, stdout=-1),
        mock.call().communicate()])
