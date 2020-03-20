import builtins
from random import choice

from colorama import init, Fore, Back

colors = (Fore.CYAN, Fore.LIGHTRED_EX, Fore.YELLOW, Fore.MAGENTA, Fore.GREEN, Fore.LIGHTCYAN_EX,
          Fore.LIGHTGREEN_EX, Fore.LIGHTMAGENTA_EX, Fore.LIGHTWHITE_EX, Fore.LIGHTYELLOW_EX, Fore.WHITE)
init()
builtins.print(Back.BLACK)


def print(*args, sep='', end='\n', center=1, color=1):
    if color:
        builtins.print(choice(colors), end='')
    else:
        builtins.print(Fore.LIGHTWHITE_EX, end='')

    if center:
        args = map(lambda x: x if x == '\n' else x.center(120), args)
    builtins.print(*args, sep=sep, end=end)
