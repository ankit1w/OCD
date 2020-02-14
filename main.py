from os import system, remove, path
from tempfile import gettempdir

from course_scraper import lecture_links, lecture_name, _MEIPASS
from animation import blink
from shutil import copyfile, rmtree
import glob

blink('Printing gathered pages to PDF...')

if len(lecture_links) == 1:
    cli_arguments = '-L 0mm -R 0mm -T 0mm -B 0mm ' + ' '.join(lecture_links)
    system(f'{_MEIPASS}\\wkhtmltopdf.exe {cli_arguments} {_MEIPASS}\\a_very_random_name_FINAL.pdf')
else:
    cli_arguments = '-L 0mm -R 0mm -T 0mm -B 0mm --page-width 350mm --page-height 10000mm --dpi 600 --zoom 2 ' + ' '.join(
        lecture_links)
    system(f'{_MEIPASS}\\wkhtmltopdf.exe {cli_arguments} {_MEIPASS}\\a_very_random_name.pdf')

    print()
    blink('Adjusting margins...\r')

    from pdfCropMargins_mod.main_pdfCropMargins import main_crop
    main_crop()
    remove(f'{_MEIPASS}\\a_very_random_name.pdf')

copyfile(f'{_MEIPASS}\\a_very_random_name_FINAL.pdf', f'{lecture_name}.pdf')
remove(f'{_MEIPASS}\\a_very_random_name_FINAL.pdf')
remove(f'{gettempdir()}\\phantomjs.exe')

for dir_path in glob.iglob(path.join(gettempdir(), "pdfCropMarginsTmpDir_*")):
    if path.isdir(dir_path):
        rmtree(dir_path)

input('Thanks for using the program!')
