import paramiko                                                         # a lib for SSH client/server connections (SSHv2 protocol)

# establishing SSH connection and command execution
def ssh_command(ip, port, user, passwd, cmd):                       
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())        # ATTENTION! Accepts the server's host key w/o verification. Unsafe for production - strong MITM risk! 
    client.connect(ip, port=port, username=user, password=passwd)

    _, stdout, stderr = client.exec_command(cmd)
    output = stdout.readlines() + stderr.readlines()
    if output:
        print('--- Output ---')
        for line in output:
            print(line.strip())

if __name__ == '__main__':
    import getpass                                                      # lazy import for the module that prompts for a password w/o echoing the characters to the terminal
    # user = getpass.getuser()                                          # uncomment to retrieve the login of the user who is running this script 
    user = input('Username: ')
    password = getpass.getpass()

    ip = input('Enter server IP: ') or '192.168.204.139'
    port = input('Enter port or <CR>: ') or 2222                        # press Enter to set it to the default value 
    cmd = input('Enter command or <CR>: ') or 'id'
    ssh_command(ip, port, user, password, cmd)
