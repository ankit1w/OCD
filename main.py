from msvcrt import getch
from os import system, _exit
from random import choices
from shutil import copyfile
from string import ascii_letters, digits
from tempfile import gettempdir
from threading import Thread
from time import sleep

from animation import animate
from cleanup import cleanup
from course_scraper import course_scraper
from path_vars import work_dir, phantomjs_path
from print_pdf import print_to_pdf

try:
    t = Thread(target=system, args=(fr'{work_dir}\disable_quick_edit.bat 2 >nul',))
    t.start()

    system('title Online Courseware Downloader')

    dummy = ''.join(choices(ascii_letters + digits, k=10))
    dummy_error = system(f'2>nul ( >{dummy} type nul)')

    if dummy_error:
        print('Could not attain permissions to create PDF in the current location.'.center(120))
        print('Make sure the folder is writable without administrative access.'.center(120))
        print('If not, run the program as administrator.'.center(120))
        raise SystemExit

    system(f'del {dummy}')

    system('mode con cols=125 lines=30')
    system('powershell -command "&{$H=get-host;$W=$H.ui.rawui;$B=$W.buffersize;'
           '$B.width=125;$B.height=450;$W.buffersize=$B;}">nul')
    system('color 0f')
    if phantomjs_path != '.':
        try:
            copyfile(fr'{work_dir}\phantomjs.exe', fr'{gettempdir()}\phantomjs.exe')
        except PermissionError:
            pass

    print('Online Courseware Downloader'.center(120))
    print('github.com/ankit1w/OCD'.center(120))
    print('─' * 125)

    lecture_name, lecture_links, new_type = course_scraper()
    print_error = print_to_pdf(lecture_links, lecture_name, new_type)

    system(f'title Online Courseware Downloader : Downloaded ↓ {lecture_name}'.replace('&', '^&'))
    system('cls')

    print('\n', f'{lecture_name}.pdf saved to current directory.'.center(120), '\n')

    if print_error:
        print('The file is possibly incomplete due to missing resources.'.center(120))

    print(open(fr'{work_dir}\dino.txt').read())
    raise SystemExit

except KeyboardInterrupt:
    animate(end=1)
    print('\n', 'Received KeyboardInterrupt!'.center(120))

    for i in range(5, 0, -1):
        print(f'Quitting in {i} seconds'.center(120), end='\r')
        sleep(1)

    try:
        raise SystemExit
    except SystemExit:
        _exit(0)

except SystemExit as e:
    if not str(e):
        print('Press any key to quit.'.center(120))
        getch()

except Exception as e:
    animate(end=1)
    print('Unknown error occurred :('.center(120))
    try:
        with open('ocd_error_log.txt', 'a') as error_log:
            error_log.write(str(e))
        print("Please share the log file 'ocd_error_log.txt' with the developer at ankit.m@my.com".center(120))
    except:
        pass

    print('Press any key to quit.'.center(120))
    getch()

finally:
    cleanup()
