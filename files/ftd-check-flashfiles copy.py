import pexpect

ssh = pexpect.spawn('ssh kumaras-adm@10.67.252.11')

try:
    ssh.expect(['Password:', 'password:', 'Enter password:'], timeout=60)
    ssh.sendline('Newyork$5775123455775')  # Replace with the actual password

    # Handle subsequent prompts
    ssh.expect(['Last login:', 'Cisco Firepower'], timeout=60)
    
    # Detect '>' prompt
    ssh.expect('>', timeout=60)
    ssh.sendline('expert')
    
    # Capture all output before 'BOSLOFW011:~$' prompt
    output = ""
    while True:
        index = ssh.expect(['BOSLOFW011:~\$', '>', pexpect.EOF, pexpect.TIMEOUT], timeout=300)
        output += ssh.before.decode()  # Append the output before prompt change
        if index == 0:
            break  # Break when the target prompt is reached
    
    print("Output before 'BOSLOFW011:~$' prompt:\n", output)
    
    # Perform 'exit' command after 'expert' command
    ssh.sendline('exit')
    ssh.expect('>', timeout=60)
    command_output = ssh.before.decode()  # Decode the output from bytes to string
    print("Command output:\n", command_output)
except pexpect.exceptions.TIMEOUT as e:
    print("Timeout occurred:", e)
except Exception as e:
    print("Error occurred:", e)

ssh.close()
