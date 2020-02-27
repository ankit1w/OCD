from random import randrange, choice
from threading import Thread
from time import sleep

from colorama import init, Fore

running = False
colors = (
    Fore.CYAN, Fore.LIGHTRED_EX, Fore.YELLOW, Fore.MAGENTA, Fore.GREEN, Fore.LIGHTCYAN_EX,
    Fore.LIGHTGREEN_EX, Fore.LIGHTMAGENTA_EX, Fore.LIGHTWHITE_EX, Fore.LIGHTYELLOW_EX, Fore.WHITE)
init()


def scrambler(animation_text):
    chars = '#*@!?$%+&'
    animation_text = animation_text.split()

    while True:
        text = list()
        for word in animation_text:
            word = list(word)
            word[randrange(len(word))] = choice(chars)
            text.append(''.join(word))
        if running:
            print(choice(colors) + ' '.join(text).center(120), end='\r')
            sleep(0.05)
        else:
            return


def animate(message_text=' ' * 120, end=0):
    global running
    if not end:
        running = True
        t = Thread(target=scrambler, args=(message_text,))
        t.start()
    else:
        running = False
        sleep(0.1)
        blink(message_text)


def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(choice(colors) + '\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')
    if iteration == total:
        print('\rLectures loaded!')


def blink(message):
    print('\r' + choice(colors) + message.center(120, ' '), end='\r')
    sleep(0.3)
    print(' ' * 120, end='\r')
    sleep(0.2)
    print('\r' + choice(colors) + message.center(120), end='\r')
    sleep(0.1)
    print(' ' * 120, end='\r')
    sleep(0.1)
    print(choice(colors) + message.center(120))
