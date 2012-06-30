import os.path
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class ExecHandler(FileSystemEventHandler):
    def __init__(self, file_name):
        self.file_name = os.path.abspath(file_name)
        sys.path.append(os.path.dirname(self.file_name))

    def on_modified(self, event):
        cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        hr = '-' * 10
        try:
            if event.src_path == self.file_name:
                print("\n%s %s %s" % (hr, cur_time, hr))
                with open(self.file_name) as f:
                    cpl = compile(f.read(), self.file_name, 'exec')
                    exec(cpl, globals(), locals())
        except Exception as e:
            print e


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: %s <file_name>" % os.path.basename(__file__))
        print("where <file_name> is python script to execute on each update.")
        exit()

    file_name = sys.argv[1]

    try:
        event_handler = ExecHandler(file_name)
        observer = Observer()
        observer.schedule(event_handler, path=os.path.dirname(file_name))
        print("Watching %s..." % file_name)
        observer.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
    except Exception as e:
        print("Error opening '%s': %s" % (file_name, e))
        exit(1)
