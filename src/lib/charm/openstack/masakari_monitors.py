import collections
import socket
import subprocess
import tempfile

import charmhelpers.core.hookenv as hookenv
import charms_openstack.adapters
import charms_openstack.charm
import charms_openstack.ip as os_ip
import charmhelpers.contrib.openstack.utils as ch_os_utils
import charms.reactive.relations as relations

charms_openstack.charm.use_defaults('charm.default-select-release')

@charms_openstack.adapters.config_property
def hostname(config):
    return socket.getfqdn()

@charms_openstack.adapters.config_property
def bob(config):
    return socket.fqdn()

class MasakariMonitorsCharm(charms_openstack.charm.OpenStackCharm):

    # Internal name of charm
    service_name = name = 'masakari'

    # First release supported
    release = 'rocky'

    # List of packages to install for this charm
    packages = ['nova-common']

    #services = ['masakari-hostmonitor', 'masakari-instancemonitor', 'masakari-processmonitor']
    services = []

    required_relations = ['identity-credentials']

    restart_map = {
        '/etc/masakarimonitors/masakarimonitors.conf': services,
        '/etc/masakarimonitors/process_list.yaml': services,
    }

    release_pkg = 'nova-common'

    package_codenames = {
        'masakari-common': collections.OrderedDict([
            ('2', 'mitaka'),
            ('3', 'newton'),
            ('4', 'ocata'),
        ]),
    }

    def request_credentials(self):
        keystone_relation = relations.endpoint_from_flag('identity-credentials.connected')
        keystone_relation.request_credentials(
            'masakari-monitors',
            project='services')

    # XXX THIS IS A TEMPORARY WORKAROUND AND SHOULD NOT BE INCLUDED IN
    # ANY DEPLOYMENTS OTHER THAN POCs
    def install(self):
        super(MasakariMonitorsCharm, self).install()
        os_release = ch_os_utils.get_os_codename_package('nova-common')
        with tempfile.TemporaryDirectory() as tmpdirname:
            git_dir = '{}/masakari'.format(tmpdirname)
            subprocess.check_call([
                'git', 'clone', '-b', 'stable/{}'.format(os_release),
                'https://github.com/openstack/masakari-monitors.git', git_dir])
            subprocess.check_call([
                'sudo', 'python3', 'setup.py', 'install'], cwd=git_dir)
#        subprocess.check_call(['mkdir', '-p', '/var/lock/masakari', '/var/log/masakari', '/var/lib/masakari'])
#        subprocess.check_call(['cp', 'templates/masakari-engine.service', '/lib/systemd/system'])
#        subprocess.check_call(['cp', 'templates/wsgi.py', '/usr/local/lib/python3.6/dist-packages/masakari/api/openstack/wsgi.py'])
#        subprocess.check_call(['systemctl', 'daemon-reload'])
#        subprocess.check_call(['systemctl', 'start', 'masakari-engine'])
#        subprocess.check_call(['cp', 'templates/api-paste.ini', '/etc/masakari/'])
