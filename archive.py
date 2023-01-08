import os
import hashlib
from random import randint, choice
from datetime import datetime

class Archive:

    def __init__(self, filename='', contributor='', ctime=True, filepath='', md5=''):
        self.contributor = contributor
        self.id = str(randint(0, 99999)).rjust(5, '0')
        self.filepath = filepath
        if ctime and isinstance(ctime, bool):
            self.date_added = datetime.now()
        else:
            self.date_added = ctime
        if filename == '':
            self.filename = os.path.basename(filepath)
        else:
            self.filename = filename

def get_archive_stats(archive_name='archive', archive_dict={}, debug=True):
    
    debug_names = ['mary tan', 'john yeo', 'alex fong', 'susan low']
    files = os.listdir(archive_name)
    for file in files:
        info = {}
        info['abs_path'] = os.path.join(os.getcwd(), archive_name, file)
        info['rel_path'] = os.path.join(archive_name, file)
        info['id'] = str(randint(0, 99999)).rjust(5, '0')
        info['ctime'] = datetime.fromtimestamp(os.path.getctime(info['abs_path']))
        info['contributor'] = choice(debug_names).upper() if debug else 'NULL'
        with open(info['abs_path'], 'rb') as f:
            b = f.read()
            info['md5hash'] = hashlib.md5(b).hexdigest()
            info['sha256hash'] = hashlib.sha256(b).hexdigest()
        archive_dict[file] = info

    return archive_dict

if __name__ == '__main__':
    
    test_obj = Archive(
        contributor='Samuel Seah',
        filepath='D:/backups/testfile.pdf'
    )

    print(vars(test_obj))

    print(get_archive_stats())



    