import collections
import socket

import charms_openstack.adapters
import charms_openstack.charm
import charms.reactive.relations as relations
import charmhelpers.core.hookenv as hookenv

charms_openstack.charm.use_defaults('charm.default-select-release')

MONITORING_INTERVAL_MIN = 10
MONITORING_INTERVAL_MAX = 300
MONITORING_INTERVAL_DEFAULT = 60
MONITORING_SAMPLES_MIN = 1
MONITORING_SAMPLES_MAX = 5
MONITORING_SAMPLES_DEFAULT = 1


@charms_openstack.adapters.config_property
def hostname(config):
    return socket.getfqdn()


@charms_openstack.adapters.config_property
def validated_monitoring_interval(cls):
    value = hookenv.config('monitoring-interval')
    if not (MONITORING_INTERVAL_MIN <= value <= MONITORING_INTERVAL_MAX):
        hookenv.log(
            "monitoring-interval={} is outside of the supported range "
            "({}-{} seconds); falling back to the default of {} "
            "seconds".format(
                value, MONITORING_INTERVAL_MIN, MONITORING_INTERVAL_MAX,
                MONITORING_INTERVAL_DEFAULT),
            level=hookenv.WARNING)
        return MONITORING_INTERVAL_DEFAULT
    return value


@charms_openstack.adapters.config_property
def validated_monitoring_samples(cls):
    value = hookenv.config('monitoring-samples')
    if not (MONITORING_SAMPLES_MIN <= value <= MONITORING_SAMPLES_MAX):
        hookenv.log(
            "monitoring-samples={} is outside of the supported range "
            "({}-{}); falling back to the default of {}".format(
                value, MONITORING_SAMPLES_MIN, MONITORING_SAMPLES_MAX,
                MONITORING_SAMPLES_DEFAULT),
            level=hookenv.WARNING)
        return MONITORING_SAMPLES_DEFAULT
    return value


class MasakariMonitorsCharm(charms_openstack.charm.OpenStackCharm):

    # Internal name of charm
    service_name = name = 'masakari'

    # First release supported
    release = 'rocky'

    # List of packages to install for this charm
    packages = ['masakari-host-monitor', 'masakari-instance-monitor']

    services = ['masakari-host-monitor', 'masakari-instance-monitor']

    required_relations = ['identity-credentials']

    restart_map = {
        '/etc/masakarimonitors/masakarimonitors.conf': services,
    }

    release_pkg = 'masakari-monitors-common'

    group = 'masakarimonitors'

    package_codenames = {
        'masakari-common': collections.OrderedDict([
            ('2', 'mitaka'),
            ('3', 'newton'),
            ('4', 'ocata'),
            ('5', 'pike'),
            ('6', 'rocky'),
            ('7', 'stein'),
            ('8', 'train'),
            ('9', 'ussuri'),
            ('10', 'victoria'),
        ]),
    }

    def request_credentials(self):
        keystone_relation = relations.endpoint_from_flag(
            'identity-credentials.connected')
        keystone_relation.request_credentials(
            'masakari-monitors',
            project='services')

    def install(self):
        super(MasakariMonitorsCharm, self).install()
