from glob import iglob
from os import remove, path
from shutil import rmtree
from sys import _MEIPASS
from tempfile import gettempdir


def cleanup():
    try:
        remove(f'{gettempdir()}\\phantomjs.exe')
        remove(f'{gettempdir()}\\disable_quick_edit.exe')
    except (FileNotFoundError, PermissionError) as _:
        pass

    for dir_path in iglob(path.join(gettempdir(), "pdfCropMarginsTmpDir_*")):
        if path.isdir(dir_path):
            try:
                rmtree(dir_path)
            except:
                pass

    for dir_path in iglob(path.join(gettempdir(), "_MEI*")):
        if path.isdir(dir_path) and dir_path != _MEIPASS:
            try:
                rmtree(dir_path)
            except PermissionError:
                pass

    for dir_path in iglob(path.join(gettempdir(), "tmp*")):
        if path.isdir(dir_path + '\\gen_py'):
            try:
                rmtree(dir_path)
            except PermissionError:
                pass
