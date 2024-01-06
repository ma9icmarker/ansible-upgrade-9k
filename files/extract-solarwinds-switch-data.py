import re
import json

def parse_file_content(file_path):
    # Regular expression patterns
    switch_info_pattern = re.compile(r'(\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2} [AP]M) on (\S+) \(([\d.]+)\)')
    inventory_line_pattern = r'^(NAME|DESCR|PID|VID|SN):'
    inventory_keys = ["NAME", "DESCR", "PID", "VID", "SN"]

    switches = {}
    current_switch = None
    inventory_item = {}

    with open(file_path, 'r') as file:
        for line in file:
            if switch_info := switch_info_pattern.match(line):
                # Save the last switch and start a new one
                if current_switch:
                    if inventory_item:
                        current_switch['inventory'].append(inventory_item)
                        inventory_item = {}
                    switches[current_hostname] = current_switch

                current_hostname = switch_info.group(2)
                current_switch = {
                    'datetime': switch_info.group(1),
                    'ip': switch_info.group(3),
                    'inventory': []
                }

            elif re.search(inventory_line_pattern, line):
                key, value = [x.strip() for x in line.split(':', 1)]
                if key == "NAME" and inventory_item:
                    # Add the completed item to inventory and start a new one
                    current_switch['inventory'].append(inventory_item)
                    inventory_item = {}

                if key in inventory_keys:
                    # Special handling for PID line to separate VID and SN
                    if key == "PID":
                        parts = value.split(',')
                        inventory_item["PID"] = parts[0].strip()
                        if len(parts) > 1 and len(parts[1].split()) > 1:
                            inventory_item["VID"] = parts[1].split()[1]
                        if len(parts) > 2 and len(parts[2].split()) > 1:
                            inventory_item["SN"] = parts[2].split()[1]
                    else:
                        inventory_item[key] = value.strip('"')

    # Add the last item and switch
    if inventory_item:
        current_switch['inventory'].append(inventory_item)
    if current_switch:
        switches[current_hostname] = current_switch

    return switches

# Set the file path for 'extract.txt'
file_path = 'extract.txt'
parsed_data = parse_file_content(file_path)

# Output file
output_file = 'switch_output.json'

# Write the parsed data to the output file in JSON format
with open(output_file, 'w') as file:
    json.dump(parsed_data, file, indent=4)
