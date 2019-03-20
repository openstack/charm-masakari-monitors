# Copyright 2019 Canonical Ltd
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

from __future__ import absolute_import
from __future__ import print_function

import mock

import reactive.masakari_monitors_handlers as handlers

import charms_openstack.test_utils as test_utils


class TestRegisteredHooks(test_utils.TestRegisteredHooks):

    def test_hooks(self):
        defaults = [
            'charm.installed',
            'config.changed',
            'update-status']
        hook_set = {
            'when': {
                'render_config': ('identity-credentials.available.auth', ),
                'request_credentials': ('identity-credentials.connected', )}
        }
        self.registered_hooks_test_helper(handlers, hook_set, defaults)


class TestHandlers(test_utils.PatchHelper):

    def _patch_provide_charm_instance(self):
        masakari_monitors_charm = mock.MagicMock()
        self.patch('charms_openstack.charm.provide_charm_instance',
                   name='provide_charm_instance',
                   new=mock.MagicMock())
        self.provide_charm_instance().__enter__.return_value = \
            masakari_monitors_charm
        self.provide_charm_instance().__exit__.return_value = None
        return masakari_monitors_charm

    def test_request_credentials(self):
        masakari_charm = self._patch_provide_charm_instance()
        handlers.request_credentials()
        masakari_charm.request_credentials.assert_called_once_with()

    def test_render_config(self):
        self.patch('charms.reactive.set_state', name='set_state')
        masakari_charm = self._patch_provide_charm_instance()
        handlers.render_config('keystone')
        masakari_charm.render_with_interfaces.assert_called_once_with(
            ('keystone',))
        masakari_charm.assess_status.assert_called_once_with()
        self.set_state.assert_called_once_with('config.rendered')
