#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from ansible.module_utils.basic import AnsibleModule

def extract_hostnames_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return list(data.keys())

def main():
    module_args = {
        'json_file': {'type': 'str', 'required': True},
        'expected_devices_file': {'type': 'str', 'required': True}
    }

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    json_file = module.params['json_file']
    expected_devices_file = module.params['expected_devices_file']

    try:
        hostnames = extract_hostnames_from_json(json_file)

        with open(expected_devices_file, 'r') as f:
            expected_devices = set(f.read().splitlines())

        missing_devices = expected_devices - set(hostnames)

        if missing_devices:
            message = f"Missing devices found: {', '.join(missing_devices)}"
            module.exit_json(changed=True, message=message, missing_devices=list(missing_devices))
        else:
            module.exit_json(changed=False, message="No missing devices found")

    except Exception as e:
        module.fail_json(msg=f"Error processing file: {str(e)}")

if __name__ == '__main__':
    main()
