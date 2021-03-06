import traceback
from msvcrt import getch
from os import system
from random import choices
from shutil import copyfile
from string import ascii_letters, digits
from tempfile import gettempdir
from threading import Thread

from animation import animate
from center_print import print
from cleanup import cleanup
from course_scraper import course_scraper
from path_vars import work_dir, phantomjs_path
from print_pdf import print_to_pdf

try:
    t = Thread(target=system, args=(fr'{work_dir}\disable_quick_edit.bat 2 >nul',))
    t.start()

    system('cls')
    dummy = ''.join(choices(ascii_letters + digits, k=10))
    dummy_error = system(f'2>nul ( >{dummy} type nul)')

    if dummy_error:
        print('Could not attain permissions to create PDF in the current location.',
              'Make sure the folder is writable without administrative access.',
              'If not, run the program as administrator.', sep='\n')
        raise SystemExit

    system(f'del {dummy}')

    system('mode con cols=125 lines=30')
    system('powershell -command "&{$H=get-host;$W=$H.ui.rawui;$B=$W.buffersize;'
           '$B.width=125;$B.height=450;$W.buffersize=$B;}">nul')

    if phantomjs_path != '.':
        try:
            copyfile(fr'{work_dir}\phantomjs.exe', fr'{gettempdir()}\phantomjs.exe')
        except PermissionError:
            pass

    system('title Online Courseware Downloader')
    print('Online Courseware Downloader', 'github.com/ankit1w/OCD', '─' * 125, sep='\n', color=0)

    lecture_name, lecture_links, new_type = course_scraper()
    print_error = print_to_pdf(lecture_links, lecture_name, new_type)

    system(f'title Online Courseware Downloader : Downloaded ↓ {lecture_name}'.replace('&', '^&'))
    system('cls')

    print('\n', f'{lecture_name}.pdf saved to current directory.', '\n')

    if print_error:
        print('The file is possibly incomplete due to missing resources.')

    print(open(fr'{work_dir}\dino.txt').read())

    print('\n', "Press any key to quit.")
    getch()

except KeyboardInterrupt:
    animate(end=1)
    print('Received KeyboardInterrupt!')

except SystemExit as e:
    if not str(e):
        print('\n', 'Press any key to quit.')
        getch()

except:
    animate(end=1)
    print('Unknown error occurred :(')
    try:
        with open('ocd_error_log.txt', 'a') as error_log:
            error_log.write(traceback.format_exc() + '\n\n')
        print("Please share the log file 'ocd_error_log.txt' with the developer at ankit.m@my.com")
    except:
        pass

    print('Press any key to quit.')
    getch()

finally:
    cleanup()
