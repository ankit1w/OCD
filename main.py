from os import system, _exit
from random import choices
from shutil import copyfile
from string import ascii_letters, digits
from sys import _MEIPASS
from tempfile import gettempdir

from colorama import init, Fore, Back

from cleanup import cleanup
from course_scraper import course_scraper
from print_pdf import print_to_pdf

init()
print(Fore.LIGHTWHITE_EX, Back.BLACK, sep='', end='')

system(f'{_MEIPASS}\\disable_quick_edit.bat 2 >nul')

dummy = ''.join(choices(ascii_letters + digits, k=10))
dummy_error = system(f'2>nul ( >{dummy} type nul)')
if dummy_error:
    print('Could not attain permissions to create PDF in the current location.')
    print('Make sure the folder is writable without administrative access.')
    print('If not, run the program as administrator.')
    print('Press any key to exit.')

    cleanup()
    system('pause>nul')
    _exit(0)
else:
    system(f'del {dummy}')

system('mode con cols=120 lines=30')
system(
    'powershell -command "&{$H=get-host;$W=$H.ui.rawui;$B=$W.buffersize;$B.width=150;$B.height=1000;$W.buffersize=$B;}">nul')
system('title Online Courseware Downloader')

try:
    copyfile(f'{_MEIPASS}\\phantomjs.exe', f'{gettempdir()}\\phantomjs.exe')
except PermissionError:
    pass

print('Online Courseware Downloader'.center(120))
print('github.com/ankit1w/OCD'.center(120))
print('─' * 120)
lecture_name, lecture_links, new_type = course_scraper()
print_to_pdf(lecture_links, lecture_name, new_type)
cleanup()

system("title Online Courseware Downloader : "
       f"Downloaded ↓ {lecture_name}".replace('&', '^&'))
print('\nThanks for using the program!')
system('pause>nul')
