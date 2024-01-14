import re
import json
from ansible.module_utils.basic import AnsibleModule

def parse_file_content(file_path):
    switch_info_pattern = re.compile(r'(\d{1,2}/\d{1,2}/\d{4} \d{1,2}:\d{2}:\d{2} [AP]M) on (\S+) \(([\d.]+)\)')
    general_inventory_pattern = re.compile(r'^NAME: "(.*)", DESCR: "(.*)"\nPID: (.*?), +VID: (.*?)(?:, +SN: (.*))?$', re.MULTILINE)
    nexus_pattern = re.compile(r'^NAME: "(.*)", +DESCR: "(.*)"\nPID: (.*?), +VID: (.*?), +SN: (.*)$', re.MULTILINE)
    firewall_pattern = re.compile(r'^Name: "(.*)", DESCR: "(.*)"\nPID: (.*?), +VID: (.*?), +SN: (.*)$', re.MULTILINE)
    wlc_5508_pattern = re.compile(r'NAME: "([^"]+)", +DESCR: "([^"]+)"\nPID: ([^,]+), +VID: ([^,]+), +SN: (\S+)', re.MULTILINE)

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

        inventory_content = content[inventory_start:inventory_end]

        # Determine the pattern to use based on the device type
        if "Nexus" in inventory_content:
            pattern = nexus_pattern
        elif "Firepower" in inventory_content:
            pattern = firewall_pattern
        elif "AIR-CT5508-K9" in inventory_content:
            pattern = wlc_5508_pattern
        else:
            pattern = general_inventory_pattern

        for item in pattern.finditer(inventory_content):
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
