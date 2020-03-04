import sys
from os import system
from random import choices
from shutil import copyfile
from string import ascii_letters, digits
from tempfile import gettempdir
from threading import Thread

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
        print('Press any key to exit.'.center(120))

        cleanup()
        system('pause>nul')
        sys.exit(0)
    else:
        system(f'del {dummy}')

    system('mode con cols=125 lines=30')
    system('powershell -command "&{$H=get-host;$W=$H.ui.rawui;$B=$W.buffersize;'
           '$B.width=125;$B.height=450;$W.buffersize=$B;}">nul')
    system('color 0F')

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
    cleanup()

    system(f"title Online Courseware Downloader : Downloaded ↓ {lecture_name}".replace('&', '^&'))
    system('cls')

    print()
    print(f'{lecture_name}.pdf saved to current directory.'.center(120))
    print()
    if print_error:
        print('The file is possibly incomplete due to connections errors.'.center(120))
    print(
        "                                                                                ____ \n"
        "                                     ___                                      .-~    '. \n"
        "                                    `-._~-.                                  / /  ~@\   ) \n"
        "                                         \  \     Thanks for using          | /  \~\.  `\ \n"
        "                                         ]  |       the program            /  |  |< ~\(..) \n"
        "                                        /   !                        _.--~T   \  \<   .,, \n"
        "                                       /   /                 ____.--~ .    _  /~\ \< / \n"
        "                                      /   /             .-~~'        /|   /o\ /-~\ \_| \n"
        "                                     /   /             /     )      |o|  / /|o/_   '--' \n"
        "                                    /   /           .-'(     l__   _j \_/ / /\|~    . \n"
        "                                    /    l          /    \       ~~~|    `/ / / \.__/l_ \n"
        "                                    |     \     _.-'      ~-\__     l      /_/~-.___.--~ \n"
        "                                    |      ~---~           /   ~~'---\_    __[o, \n"
        "                                    l  .                _.    ___     _>-/~ \n"
        "                                    \  \     .      .-~   .-~   ~>--'  / \n"
        "                                     \  ~---'            /         _.-' \n"
        "                                      '-.,_____.,_  _.--~\     _.-~ \n"
        "                                                  ~~     (   _} \n"
        "                                                         `. ~( \n"
        "                                                           )  \ \n"
        "                                                     /,`--'~\--'~\ \n")
    print('Press any key to exit.'.center(120))

    system('pause>nul')
except KeyboardInterrupt:
    print('\n')
    print('Received KeyboardInterrupt!'.center(120))
    print('Quitting in 5 seconds...'.center(120))
    system('timeout 5 >nul')
except SystemExit:
    pass
except:
    print('Unknown error occurred.')
finally:
    sys.exit(0)
