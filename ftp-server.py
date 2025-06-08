import socket
import os
import logging

'''
Настройка логирования
'''
logging.basicConfig(
    filename='server.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

'''
pwd - показывает название рабочей директории
ls - показывает содержимое текущей директории
cat <filename> - отправляет содержимое файла
create <filename> <content> - создает файл с содержимым
rm <filename> - удаляет файл
mkdir <dirname> - создает директорию
rmdir <dirname> - удаляет директорию
rename <oldname> <newname> - переименовывает файл/директорию
upload - загружает файл на сервер
download <filename> - скачивает файл с сервера
'''

dirname = os.path.join(os.getcwd(), 'docs')

def is_safe_path(basedir, path):
    return os.path.realpath(path).startswith(os.path.realpath(basedir))

def process(req):
    try:
        logging.info(f'Request: {req}')
        
        if req == 'pwd':
            response = dirname
        elif req == 'ls':
            response = '; '.join(os.listdir(dirname))
        elif req.startswith('cat '):
            filename = req.split()[1]
            filepath = os.path.join(dirname, filename)
            if not is_safe_path(dirname, filepath):
                response = 'Access denied'
            else:
                try:
                    with open(filepath, 'r') as f:
                        response = f.read()
                except:
                    response = 'File not found'
        # ... (остальные команды остаются без изменений)
        else:
            response = 'bad request'
            
        logging.info(f'Response: {response}')
        return response
        
    except Exception as e:
        error_msg = f'Error: {str(e)}'
        logging.error(error_msg)
        return error_msg

PORT = 6666

sock = socket.socket()
sock.bind(('', PORT))
sock.listen()
print("Прослушиваем порт", PORT)

while True:
    conn, addr = sock.accept()
    
    request = conn.recv(1024).decode()
    print(request)
    
    response = process(request)
    conn.send(response.encode())

conn.close()
