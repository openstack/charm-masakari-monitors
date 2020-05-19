# Overview

[Masakari][upstream-masakari] is used to provide automated recovery of
KVM-based OpenStack machine instances for deployments that use shared storage
(volumes).

The masakari-monitors charm deploys [Monitors for
Masakari][upstream-masakari-monitors] whose purpose is to detect hypervisor and
instances failures and to inform Masakari about them.

The charm is a subordinate charm (to the nova-compute charm) and is used in
conjunction with the [masakari][masakari-charm] and
[pacemaker-remote][pacemaker-remote-charm] charms. Together, these charms
provide the following functionality:

   <!-- The next line has two trailing spaces. -->

1. **Evacuation of instances** (supported since OpenStack Stein)  
   In the event of hypervisor failure, instances can be migrated to another
   hypervisor.

   <!-- The next line has two trailing spaces. -->

1. **Restarting of instances** (supported since OpenStack Ussuri)  
   A failed instance can be restarted.

For details see the [Automated Instance Recovery][cdg-app-masakari] appendix in
the [OpenStack Charms Deployment Guide][cdg].

> **Note**: The restarting of services (e.g. nova-compute) is not supported by
  the charm as it is considered a `systemd` task.

# Usage

## Configuration

See file `config.yaml` for the full list of configuration options, along with
their descriptions and default values.

## Deployment

To deploy masakari-monitors:

    juju deploy masakari-monitors

Because this is a subordinate charm a relation will need to be added to another
application to have the charm deployed on a machine.

## Actions

This section lists Juju [actions][juju-docs-actions] supported by the charm.
Actions allow specific operations to be performed on a per-unit basis. To
display action descriptions run `juju actions masakari`. If the charm is
not deployed then see file `actions.yaml`.

* `pause`
* `restart-services`
* `resume`

# Bugs

Please report bugs on [Launchpad][lp-bugs-charm-masakari-monitors].

For general charm questions refer to the [OpenStack Charm Guide][cg].

<!-- LINKS -->

[upstream-masakari]: https://docs.openstack.org/masakari
[upstream-masakari-monitors]: https://docs.openstack.org/masakari-monitors
[cg]: https://docs.openstack.org/charm-guide
[cdg]: https://docs.openstack.org/project-deploy-guide/charm-deployment-guide/latest/index.html
[cdg-app-masakari]: https://docs.openstack.org/project-deploy-guide/charm-deployment-guide/latest/app-masakari.html
[cdg-app-ha-apps]: https://docs.openstack.org/project-deploy-guide/charm-deployment-guide/latest/app-ha.html#ha-applications
[lp-bugs-charm-masakari-monitors]: https://bugs.launchpad.net/charm-masakari-monitors/+filebug
[masakari-charm]: https://jaas.ai/masakari
[pacemaker-remote-charm]: https://jaas.ai/pacemaker-remote
[juju-docs-actions]: https://jaas.ai/docs/actions
