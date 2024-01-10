#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Contributors to the Ansible project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: parse_solarwinds_data

short_description: Take raw extract from solarwinds and manipulate the data for ops reporting.

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: Long description here.

options:
  username:
    description: Username required for SSH connection
    required: true
    type: str
  ip_address:
    description: IP address of appliance to connect to
    required: true
    type: str
  password:
    description: Password required for connection
    required: true
    type: str
  commands:
    description: The shell commands to run via SSH
    required: true
    type: list
    elements: str
  expected_strings:
    description: Expeceted strings
    required: true
    type: list
    elements: str
author:
  - Swapnil AshokKumar Patel (ashok.kumar@whitecase.com)
'''

EXAMPLES = r'''
# Execute a command
- name: Connect to FTD and run show arp using custom module
  ftd_send_command:
  username: "{{ ftd.username }}"
  ip_address: "10.67.252.11"
  password: "{{ ftd.password }}"
  commands:
      - show arp
  expected_strings:
      - "statelink"
'''

RETURN = r''' # '''



import re
import json
from ansible.module_utils.basic import AnsibleModule

def parse_file_content(file_path):
    switch_info_pattern = re.compile(r'(\d{1,2}/\d{1,2}/\d{4} \d{1,2}:\d{2}:\d{2} [AP]M) on (\S+) \(([\d.]+)\)')
    inventory_pattern = re.compile(r'^NAME: "(.*)", DESCR: "(.*)"\nPID: (.*?), +VID: (.*?)(?:, +SN: (.*))?$', re.MULTILINE)

    data = {}

    with open(file_path, 'r') as file:
        content = file.read()

    for switch_info in switch_info_pattern.finditer(content):
        datetime, hostname, ip = switch_info.groups()
        switch_data = {
            "datetime": datetime,
            "hostname": hostname,
            "ip": ip,
            "inventory": []
        }

        inventory_start = switch_info.end()
        next_switch = switch_info_pattern.search(content, inventory_start)
        inventory_end = next_switch.start() if next_switch else len(content)

        for item in inventory_pattern.finditer(content, inventory_start, inventory_end):
            name, descr, pid, vid, sn = item.groups()
            switch_data["inventory"].append({
                "NAME": name.strip(),
                "DESCR": descr.strip(),
                "PID": pid.strip(),
                "VID": vid.strip(),
                "SN": sn.strip() if sn else ""
            })

        data[hostname] = switch_data

    return data

def main():
    module_args = {
        'source': {'type': 'str', 'required': True},
        'destination': {'type': 'str', 'required': True}
    }

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    source = module.params['source']
    destination = module.params['destination']

    try:
        parsed_data = parse_file_content(source)
        with open(destination, 'w') as file:
            json.dump(parsed_data, file, indent=4)
        module.exit_json(changed=True, message="File processed successfully")
    except Exception as e:
        module.fail_json(msg=f"Error processing file: {str(e)}")

if __name__ == '__main__':
    main()
