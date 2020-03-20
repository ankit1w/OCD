from random import choices
from string import ascii_letters, digits
from tempfile import gettempdir

try:
    from sys import _MEIPASS as work_dir
    temp_pdf = fr"{work_dir}\ocd_tmp_{''.join(choices(ascii_letters + digits, k=10))}"
    phantomjs_path = gettempdir()
except ImportError:
    work_dir = '.'
    temp_pdf = fr"{gettempdir()}\ocd_tmp_{''.join(choices(ascii_letters + digits, k=10))}"
    phantomjs_path = '.'
