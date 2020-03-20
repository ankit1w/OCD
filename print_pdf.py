from os import system, path, remove

from animation import animate
from center_print import print
from path_vars import work_dir, temp_pdf


class MoveFailed(Exception):
    pass


def print_to_pdf(lecture_links, lecture_name, new_type):
    try:
        print('\n', 'Printing gathered pages to PDF...')
        print()
        common_args = '-L 0mm -R 0mm -T 0mm -B 0mm --image-quality 100 -n --load-media-error-handling abort '

        if new_type:
            cli_args = common_args + ' '.join(lecture_links)
            print_error = system(fr'{work_dir}\wkhtmltopdf.exe {cli_args} "{temp_pdf}"')
        else:
            cli_args = common_args + '--page-width 350mm --page-height 10000mm -d 600 --zoom 2 ' + ' '.join(
                lecture_links)
            print_error = system(fr'{work_dir}\wkhtmltopdf.exe {cli_args} "{temp_pdf}_uncropped"')

            print()
            if path.exists(f'{temp_pdf}_uncropped'):
                animate('Adjusting margins')

                from pdfCropMargins_mod.main_pdfCropMargins import main_crop
                main_crop()
                remove(f'{temp_pdf}_uncropped')
                animate('Margins adjusted!', end=1)
            else:
                raise ConnectionError

        if path.exists(f'{temp_pdf}'):
            move_fail = system(f'move "{temp_pdf}" "{lecture_name}.pdf">nul 2>&1')
            if move_fail:
                raise MoveFailed
        else:
            raise ConnectionError
        return print_error

    except ConnectionError:
        animate(end=1)
        print('Connection Error :(')
        raise SystemExit

    except MoveFailed:
        print('\n', 'Could not attain permissions to create PDF in the current location.')
        print("Make sure an already existing PDF isn't open in a running program,"
              " or administrative rights are not required.", '\n')
        raise SystemExit
