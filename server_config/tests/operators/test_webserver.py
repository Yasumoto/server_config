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

import time
import unittest

from server_config.operators.webserver import WebserverOperator

import arrow
from freezegun import freeze_time
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
  @mock.patch('server_config.executors.webserver.WebserverExecutor.create_directory',
      autospec=True, spec_set=True)
  def test_preflight_check(self, mock_create_directory, mock_install_packages):
    self.operator.preflight_check()

    assert_equals(mock_create_directory.mock_calls, [mock.call(self.operator.executor,
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
    assert_equals(mock_application_version.mock_calls, [mock.call(self.operator.executor, hostname,
        self.operator.SYMLINK_LOCATION) for hostname in HOSTNAMES])

  @freeze_time('2016-02-20')
  @mock.patch('subprocess.check_call', autospec=True, spec_set=True)
  def test_build_artifact(self, mock_check_call):
    expected_version = arrow.utcnow().timestamp
    expected_path = self.operator.ARTIFACT_TEMPLATE % expected_version

    local_path, artifact_version = self.operator.build_artifact()

    assert_equals(local_path, expected_path)
    assert_equals(expected_version, artifact_version)
    assert_equals(mock_check_call.mock_calls, [mock.call(['/usr/bin/tar', '-czf', expected_path,
        'hello_world'])])

  @mock.patch('server_config.operators.webserver.open',
      mock.mock_open(read_data=FAKE_HOSTLIST), create=True)
  @mock.patch('urllib2.urlopen', mock.mock_open(read_data='Hello, world!'), create=True)
  @mock.patch('server_config.operators.webserver.WebserverExecutor',
      autospec=True, spec_set=True)
  @mock.patch('server_config.operators.webserver.WebserverOperator.build_artifact',
      autospec=True, spec_set=True)
  def test_deploy(self, mock_build_artifact, MockWebserverExecutor):
    local_path = '/Users/jimmeh/test_webserver_9001.tar.gz'
    artifact_version = '9001'
    mock_build_artifact.return_value = local_path, artifact_version
    clock = mock.create_autospec(time, spec_set=True)

    self.operator.deploy(clock)

    assert_equals(mock_build_artifact.mock_calls, [mock.call(self.operator)])
    fake_executor_calls = [mock.call()]
    for hostname in HOSTNAMES:
      fake_executor_calls += [
          mock.call().application_version(hostname, self.operator.SYMLINK_LOCATION),
          mock.call().stage_artifact(hostname, local_path, artifact_version,
              self.operator.staging_dir),
          mock.call().set_version(hostname, artifact_version, self.operator.staging_dir,
              self.operator.SYMLINK_LOCATION)]
    assert_equals(MockWebserverExecutor.mock_calls, fake_executor_calls)

  @mock.patch('server_config.operators.webserver.open',
      mock.mock_open(read_data=FAKE_HOSTLIST), create=True)
  @mock.patch('urllib2.urlopen', mock.mock_open(read_data='Nope'), create=True)
  @mock.patch('server_config.operators.webserver.WebserverExecutor',
      autospec=True, spec_set=True)
  @mock.patch('server_config.operators.webserver.WebserverOperator.build_artifact',
      autospec=True, spec_set=True)
  def test_deploy_rollback(self, mock_build_artifact, MockWebserverExecutor):
    local_path = '/Users/jimmeh/test_webserver_9001.tar.gz'
    artifact_version = '9001'
    mock_build_artifact.return_value = local_path, artifact_version
    clock = mock.create_autospec(time, spec_set=True)
    MockWebserverExecutor.return_value.application_version.return_value = '9000'

    self.operator.deploy(clock)

    assert_equals(mock_build_artifact.mock_calls, [mock.call(self.operator)])
    assert_equals(MockWebserverExecutor.mock_calls, [mock.call(),
          mock.call().application_version('hostA', self.operator.SYMLINK_LOCATION),
          mock.call().stage_artifact('hostA', local_path, artifact_version,
              self.operator.staging_dir),
          mock.call().set_version('hostA', artifact_version, self.operator.staging_dir,
              self.operator.SYMLINK_LOCATION),
          mock.call().set_version('hostA', '9000', self.operator.staging_dir,
              self.operator.SYMLINK_LOCATION)])