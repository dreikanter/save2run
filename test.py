import os
import os.path
import time


def format_size(num):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0


file_name = __file__
mt = time.ctime(os.path.getmtime(file_name))
sz = format_size(os.path.getsize(file_name))
print("%s updated: mtime: %s; size: %s" % (os.path.basename(file_name), mt, sz))
