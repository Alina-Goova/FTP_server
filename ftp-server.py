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

def is_safe_path(basedir, path):
    return os.path.realpath(path).startswith(os.path.realpath(basedir))

def process(req):
    try:
        if req == 'pwd':
            return dirname
        elif req == 'ls':
            return '; '.join(os.listdir(dirname))
        elif req.startswith('cat '):
            filename = req.split()[1]
            filepath = os.path.join(dirname, filename)
            if not is_safe_path(dirname, filepath):
                return 'Access denied'
            try:
                with open(filepath, 'r') as f:
                    return f.read()
            except:
                return 'File not found'
        # Add similar checks for all file operations
        # ...
    except Exception as e:
        return f'Error: {str(e)}'
