import paramiko
import subprocess

# Client connects to SSH-Server
def ssh_command(ip, port, user, passwd, command):
    client = paramiko.SSHClient()                                                       # creates an SSH-client object
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())                        # ATTENTION! Accepts the server's host key w/o verification. Unsafe for production - strong MITM risk!
    client.connect(ip, port=port, username=user, password=passwd)

    ssh_session =  client.get_transport().open_session()                                # establishes the encrypted connection, opening a channel
    if ssh_session.active:
        ssh_session.send(command)                                                       # we send the initial command to the remote channel
    print(ssh_session.recv(1024).decode())
    
    try:                                                                                # a loop for receiving server commands
        while True:
            command = ssh_session.recv(1024)
            cmd = command.decode()

            if cmd == 'exit':
                break
            
            try:
                cmd_output = subprocess.check_output(cmd, shell=True)                   # the client executes the received command locally and sends the output back
                ssh_session.send(cmd_output or b'okay')                                 # sends the output back over SSH channel
            except Exception as e:
                ssh_session.send(str(e).encode())
    finally:
        client.close()
    
if __name__ == '__main__':
    import getpass                                                                      # lazy import for the module that prompts for a password w/o echoing the characters to the terminal
    user = getpass.getuser()                                                            # returns your Windows username 
    password = getpass.getpass()

    ip = input('Enter server IP: ')
    port = input('Enter port: ')
    ssh_command(ip, port, user, password, 'ClientConnected')
