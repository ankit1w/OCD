from random import choices
from string import ascii_letters, digits
from tempfile import gettempdir

try:
    from sys import _MEIPASS

    work_dir = _MEIPASS
    temp_pdf = fr"{_MEIPASS}\{''.join(choices(ascii_letters + digits, k=10))}"
    phantomjs_path = gettempdir()
except:
    work_dir = '.'
    temp_pdf = fr"{gettempdir()}\{''.join(choices(ascii_letters + digits, k=10))}"
    phantomjs_path = '.'
