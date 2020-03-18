from os import system, _exit
from random import choices
from shutil import copyfile
from string import ascii_letters, digits
from tempfile import gettempdir
from threading import Thread

from animation import animate
from cleanup import cleanup
from course_scraper import UpdateAvailable
from course_scraper import course_scraper
from path_vars import work_dir, phantomjs_path
from print_pdf import print_to_pdf


class WritePermissionDenied(Exception): pass


try:
    t = Thread(target=system, args=(fr'{work_dir}\disable_quick_edit.bat 2 >nul',))
    t.start()

    system('title Online Courseware Downloader')

    dummy = ''.join(choices(ascii_letters + digits, k=10))
    dummy_error = system(f'2>nul ( >{dummy} type nul)')
    if dummy_error:
        raise WritePermissionDenied
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
    try:
        raise SystemExit
    except SystemExit:
        _exit(0)

except WritePermissionDenied:
    print('Could not attain permissions to create PDF in the current location.'.center(120))
    print('Make sure the folder is writable without administrative access.'.center(120))
    print('If not, run the program as administrator.'.center(120))

except UpdateAvailable:
    print('Press any key to launch site.'.center(120))
    system('pause>nul')
    system('start https://github.com/ankit1w/OCD/releases')

except SystemExit:
    print('Press any key to quit.'.center(120))
    system('pause>nul')

except:
    animate(end=1)
    print('Unknown error occurred.')

finally:
    cleanup()
