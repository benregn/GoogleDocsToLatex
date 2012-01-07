import errno
import os


def make_directory(file_path):
    if os.path.splitext(file_path)[1]:
        file_path = os.path.dirname(file_path)

    if not os.path.exists(file_path):
        try:
            os.makedirs(file_path)
            return True
        except OSError, e:
            if e.errno == errno.EEXIST:
                pass
    else:
        #folder existed
        return True
