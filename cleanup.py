from glob import iglob
from os import remove, path, stat
from shutil import rmtree
from tempfile import gettempdir

import fuckit

from path_vars import work_dir


@fuckit
def cleanup():
    remove(fr'{gettempdir()}\disable_quick_edit.exe')
    remove(fr'{gettempdir()}\phantomjs.exe')

    for dir_path in iglob(path.join(gettempdir(), "pdfCropMarginsTmpDir_*")):
        if path.isdir(dir_path):
            rmtree(dir_path)

    for dir_path in iglob(path.join(gettempdir(), "_MEI*")):
        if path.isdir(dir_path) and dir_path != work_dir:
            rmtree(dir_path)

    for dir_path in iglob(path.join(gettempdir(), "tmp*")):
        if path.isdir(dir_path + '\\gen_py'):
            rmtree(dir_path)

    for tmp in iglob(path.join(gettempdir(), "tmp*")):
        if len(tmp.split('\\')[-1]) == 11 and stat(tmp).st_size == 0:
            remove(tmp)

    for tmp_pdf in iglob(path.join(gettempdir(), "ocd_tmp_*")):
        remove(tmp_pdf)
