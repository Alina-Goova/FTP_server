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
    if req == 'pwd':
        return dirname
    elif req == 'ls':
        return '; '.join(os.listdir(dirname))
    elif req.startswith('cat '):
        filename = req.split()[1]
        try:
            with open(os.path.join(dirname, filename), 'r') as f:
                return f.read()
        except:
            return 'File not found'
    elif req.startswith('create '):
        parts = req.split(' ', 2)
        if len(parts) < 3:
            return 'Usage: create <filename> <content>'
        filename = parts[1]
        with open(os.path.join(dirname, filename), 'w') as f:
            f.write(parts[2])
        return f'File {filename} created'
    elif req.startswith('rm '):
        filename = req.split()[1]
        try:
            os.remove(os.path.join(dirname, filename))
            return f'File {filename} removed'
        except:
            return 'File not found'
    elif req.startswith('mkdir '):
        dirpath = req.split()[1]
        try:
            os.mkdir(os.path.join(dirname, dirpath))
            return f'Directory {dirpath} created'
        except:
            return 'Directory creation failed'
    elif req.startswith('rmdir '):
        dirpath = req.split()[1]
        try:
            os.rmdir(os.path.join(dirname, dirpath))
            return f'Directory {dirpath} removed'
        except:
            return 'Directory removal failed'
    elif req.startswith('rename '):
        parts = req.split()
        if len(parts) < 3:
            return 'Usage: rename <oldname> <newname>'
        oldname, newname = parts[1], parts[2]
        try:
            os.rename(os.path.join(dirname, oldname), 
                      os.path.join(dirname, newname))
            return f'Renamed {oldname} to {newname}'
        except:
            return 'Rename failed'
    return 'bad request'
