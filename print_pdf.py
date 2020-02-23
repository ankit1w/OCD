from os import system, _exit, path
from sys import _MEIPASS

from animation import blink
from cleanup import cleanup


def print_to_pdf(lecture_links, lecture_name, new_type):
    print()
    blink('Printing gathered pages to PDF...')
    print()

    common_args = '-L 0mm -R 0mm -T 0mm -B 0mm --image-quality 100 -n --load-error-handling ignore '

    if new_type:
        cli_args = common_args + ' '.join(lecture_links)
        system(f'{_MEIPASS}\\wkhtmltopdf.exe {cli_args} {_MEIPASS}\\a_very_random_name_FINAL.pdf')
    else:
        cli_args = common_args + '--page-width 350mm --page-height 10000mm -d 600 --zoom 2 ' + ' '.join(lecture_links)

        system(f'{_MEIPASS}\\wkhtmltopdf.exe {cli_args} {_MEIPASS}\\a_very_random_name.pdf')

        print()

        if path.exists(f'{_MEIPASS}\\a_very_random_name.pdf'):
            blink('Adjusting margins...')

            from pdfCropMargins_mod.main_pdfCropMargins import main_crop
            main_crop()
        else:
            print('Connection Error :(')
            print('Press any key to exit.')
            cleanup()
            system('pause>nul')
            _exit(0)

    if path.exists(f'{_MEIPASS}\\a_very_random_name_FINAL.pdf'):
        copy_fail = system(f'copy "{_MEIPASS}\\a_very_random_name_FINAL.pdf" "{lecture_name}.pdf">nul 2>&1')
        if copy_fail:
            print('Could not attain permissions to create PDF in the current location.')
            print("Make sure an already existing PDF isn't opened in a running program,"
                  " or administrative rights are not required.")
            print('Press any key to exit.')
            cleanup()
            system('pause>nul')
            _exit(0)
    else:
        print('Connection Error :(')
        print('Press any key to exit.')
        cleanup()
        system('pause>nul')
        _exit(0)
