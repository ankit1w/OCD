try:
    from sys import _MEIPASS
    work_dir = _MEIPASS
except:
    from os import getcwd
    work_dir = getcwd()

from tempfile import gettempdir
from string import ascii_letters, digits
from random import choices
temp_pdf = f"{gettempdir()}\\{''.join(choices(ascii_letters + digits, k=10))}"
