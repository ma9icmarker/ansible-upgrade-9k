#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Contributors to the Ansible project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: ftd_send_command

short_description: Sends commands to servers using direct SSH connection

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: Long description here.

options:
  source_dir:
    description: source directory of json files to be processed
    required: true
    type: str
  destination_dir:
    description: destination directory of json files to be processed
    required: true
    type: str

author:
  - Swapnil AshokKumar Patel (ashok.kumar@whitecase.com)
'''

EXAMPLES = r'''
# Execute a command
- name: Execute bulk JSON to CSV conversion module
    bulk_json_to_csv_module:
    source_dir: "/runner/project/files/solarwinds-extract/jsonfiles/"
    destination_dir: "/runner/project/files/solarwinds-extract/csv/"
'''

RETURN = r''' # '''

from ansible.module_utils.basic import AnsibleModule
import json
import csv
import os

def convert_json_to_csv(json_file, csv_file, site_mapping):
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)

        with open(csv_file, 'w', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(['Hostname', 'Datetime', 'IP', 'Name', 'Description', 'PID', 'VID', 'SN'])

            for hostname, switch in data.items():
                site_code = hostname[:3]
                site_name = site_mapping.get(site_code, site_code)
                for item in switch['inventory']:
                    csv_writer.writerow([
                        f"{site_name}-{hostname}",
                        switch['datetime'],
                        switch['ip'],
                        item.get('NAME', 'N/A'),
                        item.get('DESCR', 'N/A'),
                        item.get('PID', 'N/A'),
                        item.get('VID', 'N/A'),
                        item.get('SN', 'N/A')
                    ])
        return True
    except Exception as e:
        raise e

def main():
    module_args = {
        'source_dir': {'type': 'str', 'required': True},
        'destination_dir': {'type': 'str', 'required': True}
    }

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    source_dir = module.params['source_dir']
    destination_dir = module.params['destination_dir']

    site_mapping = {
        'AAC':  'aachen',
        'ABU':  'abu_dhabi',
        'AST':  'astana',
        'BEI':  'beijing',
        'BER':  'berlin',
        'BOC':  'bochum',
        'BOS':  'boston',
        'BRU':  'brussels',
        'CAI':  'cairo',
        'CHI':  'chicago',
        'DOH':  'doha',
        'DOR':  'dortmund',
        'DRE':  'dresden',
        'DUB':  'dubai',
        'DUI':  'duisburg',
        'DUS':  'dusseldorf',
        'EM1':  'emeadc',
        'ESS':  'essen',
        'FLE':  'flensburg',
        'FRA':  'frankfurt',
        'GEN':  'geneva',
        'HAM':  'hamburg',
        'HEL':  'helsinki',
        'HON':  'hong_kong',
        'HOU':  'houston',
        'IST':  'istanbul',
        'JAK':  'jakarta',
        'JOH':  'johannesburg',
        'LEI':  'leipzig',
        'LON':  'london_afh',
        'LON':  'london_obs',
        'LOS':  'los_angeles',
        'LUX':  'luxembourg',
        'MAD':  'madrid',
        'MAG':  'magdeburg',
        'MAN':  'manila',
        'MEL':  'melbourne',
        'MEX':  'mexico',
        'MIA':  'miami',
        'MIL':  'milan',
        'MOS':  'moscow',
        'MUS':  'muscat',
        'MUE':  'muenster',
        'NYC':  'new_york_1221',
        'NY2':  'nyc_l2',
        'PAL':  'palo_alto',
        'PAR':  'paris',
        'PRA':  'prague',
        'RIY':  'riyadh',
        'SAO':  'sao_paolo',
        'SEO':  'seoul',
        'SHA':  'shanghai',
        'SIN':  'singapore',
        'STO':  'stockholm',
        'SYD':  'sydney',
        'TAS':  'tashkent',
        'TAM':  'tampa',
        'TOK':  'tokyo',
        'WAR':  'warsaw',
        'WDC':  'washington_dc'
    }

    try:
        csv_files = {}
        for file_name in os.listdir(source_dir):
            if file_name.endswith('.json'):
                json_file = os.path.join(source_dir, file_name)
                with open(json_file, 'r') as f:
                    data = json.load(f)
                
                for hostname in data:
                    site_code = hostname[:3]
                    site_name = site_mapping.get(site_code, site_code)
                    if site_name not in csv_files:
                        csv_files[site_name] = open(os.path.join(destination_dir, f"{site_name}.csv"), 'w', newline='')
                        csv_writer = csv.writer(csv_files[site_name])
                        csv_writer.writerow(['Hostname', 'Datetime', 'IP', 'Name', 'Description', 'PID', 'VID', 'SN'])

                    csv_writer = csv.writer(csv_files[site_name])
                    switch = data[hostname]
                    for item in switch['inventory']:
                        csv_writer.writerow([
                            hostname,
                            switch['datetime'],
                            switch['ip'],
                            item.get('NAME', 'N/A'),
                            item.get('DESCR', 'N/A'),
                            item.get('PID', 'N/A'),
                            item.get('VID', 'N/A'),
                            item.get('SN', 'N/A')
                        ])

        # Close all the csv files
        for file in csv_files.values():
            file.close()

        module.exit_json(changed=True, msg="JSON files converted to CSV successfully")
    except Exception as e:
        for file in csv_files.values():
            file.close()
        module.fail_json(msg=f"An error occurred: {str(e)}")

if __name__ == '__main__':
    main()
