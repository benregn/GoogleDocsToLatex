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

def remove_ext_txt(file_path):
        """
        Removes the .txt file extension from Documents.
        """
        file_path_without_ext = file_path[:-4]

        # os.rename does not overwrite, so remove old copy first
        if os.path.exists(file_path_without_ext):
            os.remove(file_path_without_ext)
            os.rename(file_path, file_path_without_ext)
        else:
            os.rename(file_path, file_path_without_ext)

def check_for_tex_extension(path):
    """
    Checks if Documents have .tex extension, adds it if it doesn't.
    """
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path_without_tex = os.path.join(root, file)
            file_path_with_tex = os.path.join(root, file + ".tex")
            if not os.path.splitext(file)[1]:  # if file extension is empty
                if os.path.exists(file_path_with_tex):
                    os.remove(file_path_with_tex)
                    os.rename(file_path_without_tex, file_path_with_tex)
                else:
                    os.rename(file_path_without_tex, file_path_with_tex)
            else:
                pass
