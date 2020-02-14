from random import randrange, choice
from sys import stdout
from threading import Thread
from time import sleep

from colorama import Fore, init

running = True
colors = (
    Fore.CYAN, Fore.LIGHTRED_EX, Fore.YELLOW, Fore.MAGENTA, Fore.GREEN, Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX,
    Fore.LIGHTGREEN_EX, Fore.LIGHTMAGENTA_EX, Fore.LIGHTWHITE_EX, Fore.LIGHTYELLOW_EX, Fore.RED, Fore.WHITE)
init()


def scrambler(animation_text):
    chars = '#*@!?$%+&'
    animation_text = animation_text.split()

    while running:
        text = list()
        for word in animation_text:
            word = list(word)
            word[randrange(len(word))] = choice(chars)
            text.append(''.join(word))
        print(choice(colors) + ' '.join(text), end='\r')


def animate(message_text='', end=0):
    global running
    if not end:
        sleep(1)
        running = True
        t = Thread(target=scrambler, args=(message_text,))
        t.start()
        return
    else:
        running = False
        blink(f"\033[K{message_text}{' ' * 80}")


def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(choice(colors) + '\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')
    if iteration == total:
        print('\rLectures loaded!')


def blink(message):
    print(choice(colors) + message, end='\r')
    sleep(0.3)
    print(' ' * 80, end='\r')
    sleep(0.2)
    print(choice(colors) + message, end='\r')
    sleep(0.1)
    print(' ' * 80, end='\r')
    sleep(0.1)
    print(choice(colors) + message)
