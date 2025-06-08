import socket
import os

HOST = 'localhost'
PORT = 6666

while True:
    request = input('>')
    
    sock = socket.socket()
    sock.connect((HOST, PORT))
    
    if request.startswith('upload '):
        filename = request.split()[1]
        if not os.path.exists(filename):
            print('File not found')
            continue
        sock.send('upload'.encode())
        ready = sock.recv(1024).decode()
        if ready == 'READY':
            filesize = os.path.getsize(filename)
            sock.send(f'{filename}:{filesize}'.encode())
            with open(filename, 'rb') as f:
                sock.sendfile(f)
            print(sock.recv(1024).decode())
    elif request.startswith('download '):
        sock.send(request.encode())
        fileinfo = sock.recv(1024).decode().split(':', 1)
        if len(fileinfo) < 2:
            print(fileinfo[0])
            continue
        filename, filesize = fileinfo[0], int(fileinfo[1])
        with open(filename, 'wb') as f:
            received = 0
            while received < filesize:
                data = sock.recv(1024)
                f.write(data)
                received += len(data)
        print(f'File {filename} downloaded')
    else:
        sock.send(request.encode())
        response = sock.recv(1024).decode()
        print(response)
    
    sock.close()
