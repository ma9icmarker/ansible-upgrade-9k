import pexpect

ssh = pexpect.spawn('ssh admin@172.18.129.89')

try:
   # ssh.expect('continue connecting (yes/no/[fingerprint])?', timeout=60)
   # ssh.sendline('yes')

    ssh.expect(['Password:', 'password:', 'Enter password:'], timeout=60)
    ssh.sendline('C!sco12435')  # Replace with the actual password

    # Handle subsequent prompts
    ssh.expect(['Last login:', 'Cisco Firepower'], timeout=60)

    ssh.expect('>', timeout=60)

    ssh.sendline('show ip')
    ssh.expect('Current IP Addresses', timeout=60)
    command_output = ssh.before.decode()
    print(command_output)


    ssh.sendline('exit')
    ssh.expect(pexpect.EOF, timeout=60)

    # command_output = ssh.before.decode()
     #print("Command output after exit:\n", command_output)

except pexpect.exceptions.TIMEOUT as e:
    print("Timeout occurred:", e)
except Exception as e:
    print("Error occurred:", e)

ssh.close()