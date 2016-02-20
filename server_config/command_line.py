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

from server_config.dispatch import Dispatcher

import click

@click.command()
@click.option('--role', default='', help='Servers to operate upon')
@click.option('--action', default='status', help='Action to perform, currently `list` or `deploy`')
def main(role, action):
  """Tool used to perform actions upon hosts in production."""
  try:
    operator = Dispatcher().dispatch[role]
  except KeyError:
    print('Error! Could not find an operator defined for %s!' % role)
    print('You need a --role=<service_name>')
    print('Options are: %s' % ','.join(Dispatcher().dispatch.keys()))
    return -1

  operator.preflight_check()

  successful_hosts = []
  failed_hosts = []

  if action == 'deploy':
    operator.deploy()
  elif action == 'status':
    host_status = operator.status()
    print('Found these versions installed:')
    for hostname, version in host_status.items():
      print('%s: %s' % (hostname, version))
  else:
    print('Error! Did not recognize your target action of %s' % action)
    print('Valid actions are: status or deploy')
