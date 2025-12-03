import os
import paramiko
import socket
import sys
import threading

CWD = os.path.dirname(os.path.realpath(__file__))                                           # defines the Current Working directory where the script lives
HOSTKEY = paramiko.RSAKey(filename=os.path.join(CWD, 'test_rsa.key'))                       # demo file by paramiko: https://github.com/paramiko/paramiko/blob/main/demos/test_rsa.key - download to the folder with the ssh_server.py                                                                
                                                                                            # We use only 1 demo RSA private key file - it has all the cryptographic info needed. Plus Paramiko handles private keys directly. It can generate the public key on-the-fly from the private key when required.


# a class that inherits from ServerInterface to manage our policy about channels, auth and so on
class Server(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()
    
    def check_channel_request(self, kind, chanid):                                          # called when the client requests to open a channel
        if kind == 'session':                                                               # if the request kind is session, it allows a session (shell/exec) channel
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    
    def check_auth_password(self, username, password):                                      # to validate password authentication
        if (username == 'zero') and (password == 'cool'):                                   # ATTENTION! Replace with client's Windows username! Server will expect these credentials to accept authentication.
            return paramiko.AUTH_SUCCESSFUL

if __name__ == '__main__':
    server = '192.168.204.139'                                                              # provide your own IP-address (the machine this script is running on)
    ssh_port = 2222
    try: 
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                            # IPv4 + TCP
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)                          # Allows to reuse the address after restart 
        sock.bind((server, ssh_port))
        sock.listen(100)
        print('[+] Listening for connection ...')
        client, addr = sock.accept()
    except Exception as e:
        print('[-] Listen failed: ' + str(e))
        sys.exit(1)
    else:
        print('[+] Got a connection!', client, addr)
    
    bhSession = paramiko.Transport(client)                                                  # wraps the accepted TCP socket in a Paramiko's SSH Transport layer - for SSH handshakes, key exchange, auth etc.
    bhSession.add_server_key(HOSTKEY)
    server = Server()                                                                       # Instantiates our Server()
    bhSession.start_server(server=server)                                                   # Begins SSH protocol

    chan = bhSession.accept(20)                                                             # waits for a client to open a channel
    if chan is None:
        print('*** No channel.')
        sys.exit(1)
    
    print('[+] Authenticated!')
    print(chan.recv(1024))                                                                  # reads bytes sent by the client
    chan.send('Welcome to actor_ssh')
    try:                                                                                    # reads commands from local stdin - this makes the server interactive
        while True:
            command = input("Enter command: ")
            if command != 'exit':
                chan.send(command)
                r = chan.recv(8192)
                print(r.decode())
            else:
                chan.send('exit')
                print('exiting')
                bhSession.close()
                break
    except KeyboardInterrupt:
        bhSession.close()

