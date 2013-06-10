# Copyright (c) 2012 Red Hat, Inc.
#
# This software is licensed to you under the GNU General Public
# License as published by the Free Software Foundation; either version
# 2 of the License (GPLv2) or (at your option) any later version.
# There is NO WARRANTY for this software, express or implied,
# including the implied warranties of MERCHANTABILITY,
# NON-INFRINGEMENT, or FITNESS FOR A PARTICULAR PURPOSE. You should
# have received a copy of GPLv2 along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

"""
Contains methods related to the creation and navigation of the structure of the
Puppet branch of the CLI. This module should be used in place of the extensions
themselves creating or retrieving sections to centralize the organization of
the commands.
"""

from gettext import gettext as _

# -- constants ----------------------------------------------------------------

# Root section all puppet functionality will be located under
from pulp_puppet.extensions.admin.consumer import content

SECTION_ROOT = 'puppet'

SECTION_CONSUMER = 'consumer'
SECTION_REPO = 'repo'

SECTION_INSTALL = 'install'
SECTION_INSTALL_SCHEDULES = 'schedules'
SECTION_UPDATE = 'update'
SECTION_UPDATE_SCHEDULES = 'schedules'
SECTION_UNINSTALL = 'uninstall'
SECTION_UNINSTALL_SCHEDULES = 'schedules'

SECTION_UPLOADS = 'uploads'

SECTION_SYNC = 'sync'
SECTION_SYNC_SCHEDULES = 'schedules'
SECTION_PUBLISH = 'publish'
SECTION_PUBLISH_SCHEDULES = 'schedules'

DESC_ROOT = _('manage Puppet-related content and features')
DESC_CONSUMER = _('consumer commands')
DESC_REPO = _('repository lifecycle commands')

DESC_INSTALL = _('run or schedule a module install')
DESC_INSTALL_SCHEDULES = _('manage puppet module installation schedules')
DESC_UPDATE = _('run or schedule a module update')
DESC_UPDATE_SCHEDULES = _('manage puppet module update schedules')
DESC_UNINSTALL = _('run or schedule a module uninstall')
DESC_UNINSTALL_SCHEDULES = _('manage puppet module uninstall schedules')

DESC_UPLOADS = _('upload modules into a repository')

DESC_SYNC = _('run, schedule, or view the status of sync tasks')
DESC_SYNC_SCHEDULES = _('manage repository sync schedules')
DESC_PUBLISH = _('run, schedule, or view the status of publish tasks')
DESC_PUBLISH_SCHEDULES = _('manage repository publish schedules')

# -- creation -----------------------------------------------------------------

def ensure_puppet_root(cli):
    """
    Verifies that the root of puppet-related commands exists in the CLI,
    creating it using constants from this module if it does not.

    :param cli: CLI instance being configured
    :type  cli: pulp.client.extensions.core.PulpCli
    """
    root_section = cli.find_section(SECTION_ROOT)
    if root_section is None:
        root_section = cli.create_section(SECTION_ROOT, DESC_ROOT)
    return root_section


def ensure_consumer_structure(cli):
    # Make sure the puppet root is in place
    root_section = ensure_puppet_root(cli)

    # There's nothing dynamic about setting up the structure, so if the consumer
    # section exists, it's a safe bet it's configured with its necessary
    # subsections, so just punch out.
    consumer_section = root_section.find_subsection(SECTION_CONSUMER)
    if consumer_section is not None:
        return consumer_section

    consumer_section = root_section.create_subsection(SECTION_CONSUMER, DESC_CONSUMER)

    consumer_section.create_subsection(SECTION_INSTALL, DESC_INSTALL)
    consumer_section.create_subsection(SECTION_UPDATE, DESC_UPDATE)
    consumer_section.create_subsection(SECTION_UNINSTALL, DESC_UNINSTALL)

    # Add subsections to the install, uninstall, and update sections
    install_section = consumer_install_section(cli)
    install_section.create_subsection(SECTION_INSTALL_SCHEDULES, DESC_INSTALL_SCHEDULES)

    uninstall_section = consumer_uninstall_section(cli)
    uninstall_section.create_subsection(SECTION_UNINSTALL_SCHEDULES, DESC_UNINSTALL_SCHEDULES)

    update_section = consumer_update_section(cli)
    update_section.create_subsection(SECTION_UPDATE_SCHEDULES, DESC_UPDATE_SCHEDULES)

    return consumer_section


def ensure_repo_structure(cli):
    """
    Verifies that the repository section and all of its subsections are present
    in the CLI, creating them using constants from this module if they are not.

    :param cli: CLI instance being configured
    :type  cli: pulp.client.extensions.core.PulpCli
    """

    # Make sure the puppet root is in place
    root_section = ensure_puppet_root(cli)

    # There's nothing dynamic about setting up the structure, so if the repo
    # section exists, it's a safe bet it's configured with its necessary
    # subsections, so just punch out.
    repo_section = root_section.find_subsection(SECTION_REPO)
    if repo_section is not None:
        return repo_section

    repo_section = root_section.create_subsection(SECTION_REPO, DESC_REPO)

    # Add the direct subsections of repo
    direct_subsections = (
        (SECTION_UPLOADS, DESC_UPLOADS),
        (SECTION_SYNC, DESC_SYNC),
        (SECTION_PUBLISH, DESC_PUBLISH),
    )
    for name, description in direct_subsections:
        repo_section.create_subsection(name, description)

    # Add specific third-tier sections
    sync_section = repo_sync_section(cli)
    sync_section.create_subsection(SECTION_SYNC_SCHEDULES, DESC_SYNC_SCHEDULES)

    publish_section = repo_publish_section(cli)
    publish_section.create_subsection(SECTION_PUBLISH_SCHEDULES, DESC_PUBLISH_SCHEDULES)

    return repo_section

# -- section retrieval --------------------------------------------------------

def consumer_section(cli):
    return _find_section(cli, SECTION_ROOT, SECTION_CONSUMER)


def consumer_install_section(cli):
    return _find_section(cli, SECTION_ROOT, SECTION_CONSUMER, SECTION_INSTALL)


def consumer_install_schedules_section(cli):
    return _find_section(cli, SECTION_ROOT, SECTION_CONSUMER, SECTION_INSTALL, SECTION_INSTALL_SCHEDULES)


def consumer_update_section(cli):
    return _find_section(cli, SECTION_ROOT, SECTION_CONSUMER, SECTION_UPDATE)


def consumer_update_schedules_section(cli):
    return _find_section(cli, SECTION_ROOT, SECTION_CONSUMER, SECTION_UPDATE, SECTION_UPDATE_SCHEDULES)


def consumer_uninstall_section(cli):
    return _find_section(cli, SECTION_ROOT, SECTION_CONSUMER, SECTION_UNINSTALL)


def consumer_uninstall_schedules_section(cli):
    return _find_section(cli, SECTION_ROOT, SECTION_CONSUMER, SECTION_UNINSTALL,
                         SECTION_UNINSTALL_SCHEDULES)


def repo_section(cli):
    return _find_section(cli, SECTION_ROOT, SECTION_REPO)


def repo_uploads_section(cli):
    return _find_section(cli, SECTION_ROOT, SECTION_REPO, SECTION_UPLOADS)


def repo_sync_section(cli):
    return _find_section(cli, SECTION_ROOT, SECTION_REPO, SECTION_SYNC)


def repo_sync_schedules_section(cli):
    return _find_section(cli, SECTION_ROOT, SECTION_REPO, SECTION_SYNC, SECTION_SYNC_SCHEDULES)


def repo_publish_section(cli):
    return _find_section(cli, SECTION_ROOT, SECTION_REPO, SECTION_PUBLISH)


def repo_publish_schedules_section(cli):
    return _find_section(cli, SECTION_ROOT, SECTION_REPO, SECTION_PUBLISH, SECTION_PUBLISH_SCHEDULES)

# -- private ------------------------------------------------------------------

def _find_section(cli, *path):
    """
    Follows the given path to return the indicated section from the CLI.

    :param cli: CLI instance to search within
    :type  cli: pulp.client.extensions.core.PulpCli
    :param path: path through the nest of sections to the desired section
    :type  path: list of str
    
    :return: section instance that matches the path
    :rtype:  pulp.client.extensions.core.PulpCliSection
    """
    section = cli.root_section
    for p in path:
        section = section.find_subsection(p)
    return section
