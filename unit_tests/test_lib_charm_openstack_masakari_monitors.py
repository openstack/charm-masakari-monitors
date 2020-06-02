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

import mock

import charmhelpers

import charm.openstack.masakari_monitors as masakari_monitors

import charms_openstack.test_utils as test_utils


class Helper(test_utils.PatchHelper):

    def setUp(self):
        super().setUp()
        self.patch_release(masakari_monitors.MasakariMonitorsCharm.release)


class TestMasakariMonitorsCharm(Helper):

    def _patch_config_and_charm(self, config):
        self.patch_object(charmhelpers.core.hookenv, 'config')

        def cf(key=None):
            if key is not None:
                return config[key]
            return config

        self.config.side_effect = cf
        c = masakari_monitors.MasakariMonitorsCharm()
        return c

    def test_request_credentials(self):
        keystone_relation = mock.MagicMock()
        self.patch('charms.reactive.relations.endpoint_from_flag',
                   name='endpoint_from_flag',
                   return_value=keystone_relation)
        c = self._patch_config_and_charm({})
        c.request_credentials()
        keystone_relation.request_credentials.assert_called_once_with(
            'masakari-monitors', project='services')
