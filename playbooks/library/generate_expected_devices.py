#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from ansible.module_utils.basic import AnsibleModule

def generate_expected_devices(json_file, output_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    hostnames = list(data.keys())
    
    with open(output_file, 'w') as f:
        for hostname in hostnames:
            f.write(hostname + '\n')
    
    return hostnames

def main():
    module_args = {
        'json_file': {'type': 'str', 'required': True},
        'output_file': {'type': 'str', 'required': True}
    }

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    json_file = module.params['json_file']
    output_file = module.params['output_file']

    try:
        hostnames = generate_expected_devices(json_file, output_file)
        module.exit_json(changed=True, message="Expected devices file generated successfully", hostnames=hostnames)
    except Exception as e:
        module.fail_json(msg=f"Error: {str(e)}")

if __name__ == '__main__':
    main()
