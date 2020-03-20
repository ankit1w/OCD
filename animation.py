from random import randrange, choice
from threading import Thread
from time import sleep

from center_print import print

running = False


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
            print(' '.join(text), end='\r')
            sleep(0.05)
        else:
            return


def animate(message_text='', end=0):
    global running
    if not end:
        running = True
        t = Thread(target=scrambler, args=(message_text,))
        t.start()
    else:
        running = False
        sleep(0.1)
        if message_text:
            blink(message_text)


# printProgressBar function has been written by Greenstick at https://gist.github.com/greenstick/c34d044225293c9b191f
def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')
    if iteration == total:
        print('\r  Pages collected ', center=0)


def blink(message):
    print(message, end='\r')
    sleep(0.3)
    print(' ' * 120, end='\r')
    sleep(0.2)
    print(message, end='\r')
    sleep(0.1)
    print(' ' * 120, end='\r')
    sleep(0.1)
    print(message)
