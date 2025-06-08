import socket
import os
'''
pwd - показывает название рабочей директории
ls - показывает содержимое текущей директории
cat <filename> - отправляет содержимое файла
create <filename> <content> - создает файл с содержимым
rm <filename> - удаляет файл
'''

dirname = os.path.join(os.getcwd(), 'docs')

def process(req):
    # ... previous commands ...
    elif req == 'upload':
        conn.send('READY'.encode())
        fileinfo = conn.recv(1024).decode().split(':', 1)
        filename, filesize = fileinfo[0], int(fileinfo[1])
        with open(os.path.join(dirname, filename), 'wb') as f:
            received = 0
            while received < filesize:
                data = conn.recv(1024)
                f.write(data)
                received += len(data)
        return f'File {filename} uploaded'
    elif req.startswith('download '):
        filename = req.split()[1]
        try:
            filesize = os.path.getsize(os.path.join(dirname, filename))
            conn.send(f'{filename}:{filesize}'.encode())
            with open(os.path.join(dirname, filename), 'rb') as f:
                conn.sendfile(f)
            return 'File sent'
        except:
            return 'File not found'
    return 'bad request'
