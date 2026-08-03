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

from unittest import mock

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

    def test_validated_monitoring_interval_valid(self):
        self.patch_object(charmhelpers.core.hookenv, 'config')
        self.patch_object(charmhelpers.core.hookenv, 'log')
        self.config.return_value = 60
        value = masakari_monitors.validated_monitoring_interval(None)
        self.assertEqual(value, 60)
        self.log.assert_not_called()

    def test_validated_monitoring_interval_too_low(self):
        self.patch_object(charmhelpers.core.hookenv, 'config')
        self.patch_object(charmhelpers.core.hookenv, 'log')
        self.config.return_value = 5
        value = masakari_monitors.validated_monitoring_interval(None)
        self.assertEqual(value, masakari_monitors.MONITORING_INTERVAL_DEFAULT)
        self.log.assert_called_once()

    def test_validated_monitoring_interval_too_high(self):
        self.patch_object(charmhelpers.core.hookenv, 'config')
        self.patch_object(charmhelpers.core.hookenv, 'log')
        self.config.return_value = 301
        value = masakari_monitors.validated_monitoring_interval(None)
        self.assertEqual(value, masakari_monitors.MONITORING_INTERVAL_DEFAULT)
        self.log.assert_called_once()

    def test_validated_monitoring_samples_valid(self):
        self.patch_object(charmhelpers.core.hookenv, 'config')
        self.patch_object(charmhelpers.core.hookenv, 'log')
        self.config.return_value = 1
        value = masakari_monitors.validated_monitoring_samples(None)
        self.assertEqual(value, 1)
        self.log.assert_not_called()

    def test_validated_monitoring_samples_too_low(self):
        self.patch_object(charmhelpers.core.hookenv, 'config')
        self.patch_object(charmhelpers.core.hookenv, 'log')
        self.config.return_value = 0
        value = masakari_monitors.validated_monitoring_samples(None)
        self.assertEqual(value, masakari_monitors.MONITORING_SAMPLES_DEFAULT)
        self.log.assert_called_once()

    def test_validated_monitoring_samples_too_high(self):
        self.patch_object(charmhelpers.core.hookenv, 'config')
        self.patch_object(charmhelpers.core.hookenv, 'log')
        self.config.return_value = 6
        value = masakari_monitors.validated_monitoring_samples(None)
        self.assertEqual(value, masakari_monitors.MONITORING_SAMPLES_DEFAULT)
        self.log.assert_called_once()
