from glob import iglob
from os import remove, path
from shutil import rmtree
from tempfile import gettempdir

from path_vars import work_dir


def cleanup():
    try:
        remove(fr'{gettempdir()}\disable_quick_edit.exe')
        remove(fr'{gettempdir()}\phantomjs.exe')
    except (FileNotFoundError, PermissionError):
        pass

    for dir_path in iglob(path.join(gettempdir(), "pdfCropMarginsTmpDir_*")):
        if path.isdir(dir_path):
            try:
                rmtree(dir_path)
            except PermissionError:
                pass

    for dir_path in iglob(path.join(gettempdir(), "_MEI*")):
        if path.isdir(dir_path) and dir_path != work_dir:
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
