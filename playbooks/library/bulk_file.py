from ansible.module_utils.basic import AnsibleModule
import json
import csv
import os

def main():
    module_args = {
        'source_dir': {'type': 'str', 'required': True},
        'destination_dir': {'type': 'str', 'required': True},
        'amalgamated_file_name': {'type': 'str', 'required': False, 'default': ''}
    }

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    source_dir = module.params['source_dir']
    destination_dir = module.params['destination_dir']
    amalgamated_file_name = module.params['amalgamated_file_name']

    # Your existing site mapping
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
        create_amalgamated_file = amalgamated_file_name != ''
        if create_amalgamated_file:
            all_data_file = open(os.path.join(destination_dir, amalgamated_file_name), 'w', newline='')
            all_data_writer = csv.writer(all_data_file)
            all_data_writer.writerow(['Hostname', 'Datetime', 'IP', 'Name', 'Description', 'PID', 'VID', 'SN'])

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
                        row = [
                            hostname,
                            switch['datetime'],
                            switch['ip'],
                            item.get('NAME', 'N/A'),
                            item.get('DESCR', 'N/A'),
                            item.get('PID', 'N/A'),
                            item.get('VID', 'N/A'),
                            item.get('SN', 'N/A')
                        ]
                        csv_writer.writerow(row)
                        if create_amalgamated_file:
                            all_data_writer.writerow(row)

        # Close all the individual csv files
        for file in csv_files.values():
            file.close()

        # Close the aggregated data file if it was created
        if create_amalgamated_file:
            all_data_file.close()

        module.exit_json(changed=True, msg="JSON files converted to CSV successfully")
    except Exception as e:
        for file in csv_files.values():
            file.close()
        if create_amalgamated_file:
            all_data_file.close()
        module.fail_json(msg=f"An error occurred: {str(e)}")

if __name__ == '__main__':
    main()
