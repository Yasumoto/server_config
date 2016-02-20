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

from server_config.operators.webserver import WebserverOperator

from nose.tools import assert_equals
import mock


FAKE_HOSTLIST = '''hostA
hostB
hostC
'''

HOSTNAMES = ['hostA', 'hostB', 'hostC']

class TestWebserverOperator(unittest.TestCase):
  def setUp(self):
    self.operator = WebserverOperator()

  def test_name(self):
    assert self.operator.name is not None

  @mock.patch('server_config.operators.webserver.open',
      mock.mock_open(read_data=FAKE_HOSTLIST), create=True)
  def test_hostlist(self):
    with self.operator.hostlist() as hostlist:
      assert_equals(len(hostlist), 3)

  @mock.patch('server_config.operators.webserver.open',
      mock.mock_open(read_data=FAKE_HOSTLIST), create=True)
  @mock.patch('server_config.executors.webserver.WebserverExecutor.install_packages',
      autospec=True, spec_set=True)
  @mock.patch('server_config.executors.webserver.WebserverExecutor.create_staging_directory',
      autospec=True, spec_set=True)
  def test_preflight_check(self, mock_create_staging_directory, mock_install_packages):
    self.operator.preflight_check()

    assert_equals(mock_create_staging_directory.mock_calls, [mock.call(self.operator.executor,
        hostname, self.operator.staging_dir) for hostname in HOSTNAMES])
    assert_equals(mock_install_packages.mock_calls, [mock.call(self.operator.executor, hostname,
        self.operator.PACKAGE_LIST) for hostname in HOSTNAMES])

  @mock.patch('server_config.operators.webserver.open',
      mock.mock_open(read_data=FAKE_HOSTLIST), create=True)
  @mock.patch('server_config.executors.webserver.WebserverExecutor.application_version',
      autospec=True, spec_set=True)
  def test_status(self, mock_application_version):
    mock_application_version.return_value = 1337

    versions = self.operator.status()

    expected_versions = {}
    for hostname in HOSTNAMES:
      expected_versions[hostname] = 1337

    assert_equals(versions, expected_versions)
    assert_equals(mock_application_version.mock_calls, [mock.call(self.operator.executor, hostname)
        for hostname in HOSTNAMES])
