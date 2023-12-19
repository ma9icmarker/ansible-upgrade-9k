#!/usr/bin/python3

from ansible.module_utils.basic import AnsibleModule
import pexpect

def run_ssh_command(module):
    username = module.params['username']
    ip_address = module.params['ip_address']
    password = module.params['password']
    commands = module.params['commands']
    expected_strings = module.params['expected_strings']

    ssh_command = f'ssh {username}@{ip_address}'
    ssh = pexpect.spawn(ssh_command)

    try:
#        ssh.expect('continue connecting (yes/no/[fingerprint])?', timeout=60)
#        ssh.sendline('yes')

        ssh.expect(['Password:', 'password:', 'Enter password:'], timeout=60)
        ssh.sendline(password)

        ssh.expect(['Last login:', 'Cisco Firepower'], timeout=60)

        ssh.expect('>', timeout=60)

        command_outputs = []
        for i, command in enumerate(commands):
            ssh.sendline(command)
            ssh.expect(expected_strings[i], timeout=60)
            command_outputs.append(ssh.before.decode())

        ssh.sendline('exit')
        ssh.expect(pexpect.EOF, timeout=60)

        return True, command_outputs

    except pexpect.exceptions.TIMEOUT as e:
        return False, str(e)
    except Exception as e:
        return False, str(e)
    finally:
        ssh.close()

def main():
    module_args = {
        'username': {'type': 'str', 'required': True},
        'ip_address': {'type': 'str', 'required': True},
        'password': {'type': 'str', 'required': True},
        'commands': {'type': 'list', 'required': True},
        'expected_strings': {'type': 'list', 'required': True}
    }

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    success, output = run_ssh_command(module)

    if success:
        module.exit_json(changed=True, msg=output)
    else:
        module.fail_json(msg=output)

if __name__ == '__main__':
    main()
