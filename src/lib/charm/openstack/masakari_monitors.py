import collections
import socket

import charmhelpers.fetch
import charms_openstack.adapters
import charms_openstack.charm
import charms.reactive.relations as relations

charms_openstack.charm.use_defaults('charm.default-select-release')


@charms_openstack.adapters.config_property
def hostname(config):
    return socket.getfqdn()


class MasakariMonitorsCharm(charms_openstack.charm.OpenStackCharm):

    # Internal name of charm
    service_name = name = 'masakari'

    # First release supported
    release = 'rocky'

    # List of packages to install for this charm
    packages = ['masakari-host-monitor', 'masakari-instance-monitor',
                'masakari-process-monitor']

    services = ['masakari-host-monitor', 'masakari-instance-monitor',
                'masakari-process-monitor']

    required_relations = ['identity-credentials']

    restart_map = {
        '/etc/masakarimonitors/masakarimonitors.conf': services,
        '/etc/masakarimonitors/process_list.yaml': services,
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
        ]),
    }

    def request_credentials(self):
        keystone_relation = relations.endpoint_from_flag(
            'identity-credentials.connected')
        keystone_relation.request_credentials(
            'masakari-monitors',
            project='services')

    def install(self):
        charmhelpers.fetch.add_source('ppa:corey.bryant/bionic-stein')
        super(MasakariMonitorsCharm, self).install()
