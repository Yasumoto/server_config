#!/usr/bin/env bash
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
set -eu

if which python2.7 >/dev/null; then
  PYTHON=`which python2.7`
else
  echo 'No python 2.7 interpreter found on the path.  Please install python first' 1>&2
  exit 1
fi

if which pex >/dev/null; then
  PEX=`which pex`
else
  echo 'No pex executable found on the path.  Please "pip install pex" first' 1>&2
  exit 1
fi

if [ ! -e check.pex ]; then
  DISTUTILS_DEBUG=1 PEX_VERBOSE=1 ${PEX} twitter.checkstyle -o check.pex -c twitterstyle
fi

./check.pex --strict

${PYTHON} setup.py test

if [ -e server_config.pex ]; then
  rm -rf ~/.pex
  rm server_config.pex
fi

DISTUTILS_DEBUG=1 PEX_VERBOSE=1 ${PEX} . -c server-config -o server_config.pex
