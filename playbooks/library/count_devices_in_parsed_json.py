#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from ansible.module_utils.basic import AnsibleModule

def count_devices_in_parsed_json(json_file):
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)
        return len(data.keys())
    except Exception as e:
        raise e

def main():
    module_args = {
        'json_file': {'type': 'str', 'required': True}
    }

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    json_file = module.params['json_file']

    try:
        device_count = count_devices_in_parsed_json(json_file)
        module.exit_json(changed=False, device_count=device_count, message=f"Total number of devices: {device_count}")
    except Exception as e:
        module.fail_json(msg=f"Error processing file: {str(e)}")

if __name__ == '__main__':
    main()
