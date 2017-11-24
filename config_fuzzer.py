#!/usr/bin/env python3
"""Bootstrap configuration fuzzing.

Generates all possible configuration states resulting
from fixed and variable entries
"""

__author__ = 'pku'

from itertools import product

variable_schema = {
    'openbaton_bootstrap_version': ['latest', '4.0.0'],
    'https': ['yes', 'no'],
    'mysql': ['yes', 'no']
}

static_disabled = {
    'openbaton_installation_manner': 'noninteractive',
    'openbaton_component_autostart': 'true',
    'openbaton_vnfm_generic': 'no',
    'openbaton_fms': 'no',
    'openbaton_ase': 'no',
    'openbaton_nse': 'no',
    'openbaton_cli': 'no',
    'openbaton_plugin_vimdriver_test': 'no',
    'openbaton_plugin_vimdriver_openstack': 'no'
}
static_enabled = {
    'openbaton_installation_manner': 'noninteractive',
    'openbaton_component_autostart': 'true',
    'openbaton_vnfm_generic': 'yes',
    'openbaton_fms': 'yes',
    'openbaton_ase': 'yes',
    'openbaton_nse': 'yes',
    'openbaton_cli': 'yes',
    'openbaton_plugin_vimdriver_test': 'yes',
    'openbaton_plugin_vimdriver_openstack': 'yes'
}

static_passwords = {
    'mysql_root_password': 'mysql_password',
    'openbaton_nfvo_mysql_user': 'openbaton_user',
    'openbaton_nfvo_mysql_user_password': 'openbaton_password',
    'openbaton_fms_mysql_user': 'fms_user',
    'openbaton_fms_mysql_user_password': 'fms_password'
}


def save_configs(dicts, fixed_content, p=''):
    """Return config in a printable form."""
    for d in dicts:
        with open('cfg_' + p + '_' + '_'.join(d.values()), 'w') as output_file:
            d.update(static_disabled)
            for key, value in d.items():
                output_file.write(key+'='+value+'\n')


def generate_configs(d):
    """Gernerate cartesian product."""
    return [dict(zip(d, x)) for x in product(*d.values())]


def main():
    """Download config, evaluate arguments, print config."""
    save_configs(generate_configs(variable_schema),
                 static_disabled, p='disabled')
    save_configs(generate_configs(variable_schema)[0:1],
                 static_enabled, p='enabled')
    save_configs(generate_configs(variable_schema)[0:1],
                 static_passwords, p='password')


if __name__ == '__main__':
    main()
