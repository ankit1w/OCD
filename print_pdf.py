import sys
from os import system, path, remove

from animation import animate
from cleanup import cleanup
from path_vars import work_dir, temp_pdf


def print_to_pdf(lecture_links, lecture_name, new_type):
    print('\n', 'Printing gathered pages to PDF...'.center(120), '\n')

    common_args = '-L 0mm -R 0mm -T 0mm -B 0mm --image-quality 100 -n --load-media-error-handling abort '

    if new_type:
        cli_args = common_args + ' '.join(lecture_links)
        print_error = system(fr'{work_dir}\wkhtmltopdf.exe {cli_args} "{temp_pdf}"')
    else:
        cli_args = common_args + '--page-width 350mm --page-height 10000mm -d 600 --zoom 2 ' + ' '.join(lecture_links)

        print_error = system(fr'{work_dir}\wkhtmltopdf.exe {cli_args} "{temp_pdf}_uncropped"')

        print()

        if path.exists(f'{temp_pdf}_uncropped'):
            animate('Adjusting margins...')

            try:
                from pdfCropMargins_mod.main_pdfCropMargins import main_crop
                main_crop()
                remove(f'{temp_pdf}_uncropped')
                animate('Margins optimized!', end=1)
            except:
                animate(end=1)
                raise
        else:
            print('Connection Error :('.center(120))
            print('Press any key to exit.'.center(120))
            cleanup()
            system('pause>nul')
            sys.exit(0)

    if path.exists(f'{temp_pdf}'):
        move_fail = system(f'move "{temp_pdf}" "{lecture_name}.pdf">nul 2>&1')
        if move_fail:
            print('Could not attain permissions to create PDF in the current location.')
            print("Make sure an already existing PDF isn't opened in a running program,"
                  " or administrative rights are not required.")
            print('Press any key to exit.')
            cleanup()
            system('pause>nul')
            sys.exit(0)
    else:
        print('Connection Error :('.center(120))
        print('Press any key to exit.'.center(120))
        cleanup()
        system('pause>nul')
        sys.exit(0)

    return print_error
