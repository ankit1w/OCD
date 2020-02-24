from os import system, _exit, path, remove

from animation import blink
from cleanup import cleanup
from path_vars import work_dir, temp_pdf


def print_to_pdf(lecture_links, lecture_name, new_type):
    print()
    blink('Printing gathered pages to PDF...')
    print()

    common_args = '-L 0mm -R 0mm -T 0mm -B 0mm --image-quality 100 -n --load-error-handling ignore '

    if new_type:
        cli_args = common_args + ' '.join(lecture_links)
        system(f'{work_dir}\\wkhtmltopdf.exe {cli_args} {temp_pdf}')
    else:
        cli_args = common_args + '--page-width 350mm --page-height 10000mm -d 600 --zoom 2 ' + ' '.join(lecture_links)

        system(f'{work_dir}\\wkhtmltopdf.exe {cli_args} {temp_pdf}_uncropped')

        print()

        if path.exists(f'{temp_pdf}_uncropped'):
            blink('Adjusting margins...')

            from pdfCropMargins_mod.main_pdfCropMargins import main_crop
            main_crop()
            remove(f'{temp_pdf}_uncropped')
        else:
            print('Connection Error :(')
            print('Press any key to exit.')
            cleanup()
            system('pause>nul')
            _exit(0)

    if path.exists(f'{temp_pdf}'):
        copy_fail = system(f'move "{temp_pdf}" "{lecture_name}.pdf">nul 2>&1')
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
