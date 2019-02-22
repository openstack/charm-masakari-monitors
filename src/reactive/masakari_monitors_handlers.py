# Copyright 2016 Canonical Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import subprocess

import charms_openstack.charm as charm
import charms.reactive as reactive

# This charm's library contains all of the handler code associated with
# sdn_charm
import charm.openstack.masakari_monitors as masakari_monitors  # noqa

charm.use_defaults(
    'charm.installed',
    'config.changed',
    'update-status')

@reactive.when('identity-credentials.connected')
def request_credentials():
    with charm.provide_charm_instance() as charm_class:
        charm_class.request_credentials()

@reactive.when('identity-credentials.available.auth')
def render_config(*args):
    """Render the configuration for charm when all the interfaces are
    available.
    """
    print("Rendering ...")
    with charm.provide_charm_instance() as charm_class:
#        charm_class.upgrade_if_available(args)
        charm_class.render_with_interfaces(args)
        charm_class.assess_status()
    reactive.set_state('config.rendered')
