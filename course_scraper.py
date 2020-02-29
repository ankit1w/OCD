import sys
from os import system
from time import sleep
from warnings import filterwarnings
from threading import Thread
from requests import head, get
from selenium import common, webdriver

from animation import animate, printProgressBar, blink
from cleanup import cleanup
from path_vars import phantomjs_path

step = 0
driver = None
error_pos = {0: 'checking for updates', 1: 'starting the page render engine', 2: 'login', 3: 'gathering subjects',
             4: 'gathering the courseware',
             5: 'getting lectures'}


def check_updates():
    animate("Checking updates...")
    version = get('https://raw.githubusercontent.com/ankit1w/OCD/master/current_version', timeout=20).text[:-1]
    animate(end=1)
    return version


def check_lecture_type(lecture_1):
    return "src='Imagepath/" in get(lecture_1).text


def login():
    animate('Attempting login')

    driver.execute_script("window.location.href='http://122.252.249.26:96/forms/frmlogin.aspx'")
    total_sum = driver.find_element_by_id('cntxt_tot_sum').get_attribute('value')
    driver.find_element_by_id('ctxt_user_id').send_keys('student')
    driver.find_element_by_id('ctxt_pass_word').send_keys('student')
    driver.find_element_by_id('cntxt_sum').send_keys(total_sum)
    driver.find_element_by_id('cmd_login').click()

    animate('Login successful!', end=1)


def get_subject_list():
    animate('Getting list of subjects')

    driver.execute_script("LoadPage('frmSubjectList.aspx',0)")

    animate('Subject list loaded!', end=1)


def load_handbook():
    animate('Gathering courseware')
    subject_list = driver.find_element_by_id('ul_subject_menu').find_elements_by_tag_name('input')
    js_functions = tuple(map(lambda x: x.get_attribute('onclick'), subject_list))

    if len(js_functions) == 0:
        raise common.exceptions.NoSuchElementException

    animate('Courseware loaded!', end=1)
    for index, command in enumerate(js_functions):
        sub_name = command.split(',')[1][1:-2].split(' - ', 1)
        sub_name = (sub_name[0] + ' ').ljust(20, '─') + ' ' + sub_name[1]

        print(f'{str(index + 1).rjust(10)}. {sub_name}')

    while True:
        print()
        try:
            cmd_no = int(input(f'Enter subject number [1-{len(js_functions)}] : ')) - 1
            if cmd_no not in range(0, len(js_functions)):
                raise ValueError
            break
        except ValueError:
            print('Wrong input! Enter again.\n')

    print()
    lecture_name = js_functions[cmd_no].split(',', 1)[1][1:-2]

    system('cls')
    print('Online Courseware Downloader'.center(120))
    print('github.com/ankit1w/OCD'.center(120))
    print('─' * 125)
    blink(f"Loading...{lecture_name}")
    print()
    system("title Online Courseware Downloader : "
           f"Downloading ↓ {lecture_name}".replace('&', '^&'))

    driver.execute_script(js_functions[cmd_no])

    return lecture_name


def get_lecture_res():
    lecture_links = list()
    total_lectures = len(set(map(lambda x: x.get_attribute('value'),
                                 driver.find_element_by_id('div_navigate_session').find_elements_by_tag_name('input'))))
    lecture_page = driver.find_element_by_id('IFRAME_ID_1').get_attribute('src')
    lecture_page = lecture_page.split('#')[0]

    phantomjs_quit = Thread(target=driver.quit)
    phantomjs_quit.start()

    if head(lecture_page).status_code != 200:
        print('Lecture could not be found on server.'.center(120))
        print('Press any key to quit.'.center(120))
        cleanup()
        system('pause>nul')
        sys.exit(0)

    new_type = check_lecture_type(lecture_page)

    if total_lectures == 1:
        blink('Lecture loaded!')
        lecture_links.append(lecture_page)
        return lecture_links, new_type

    module = 1
    blink(f'{total_lectures} lectures have been found.')
    print()

    for i in range(1, total_lectures + 1):
        printProgressBar(i, total_lectures, prefix='Loading lectures', suffix='Complete', length=50)
        lecture_page = lecture_page.replace(f'_L{i - 1}', f'_L{i}')
        if head(lecture_page).status_code == 404:
            lecture_page = lecture_page.replace(f'_M{module}', f'_M{module + 1}')
            module += 1
        lecture_links.append(lecture_page)

    return lecture_links, new_type


def course_scraper():
    global step, driver
    try:
        if check_updates() != '1.0':
            print('Update available! Get the latest version from github.com/ankit1w/OCD/releases')
            print('Press any key to launch site.')
            system('pause>nul')
            system('start https://github.com/ankit1w/OCD/releases')
            sys.exit(0)

        filterwarnings('ignore')

        step += 1
        animate('Starting page render engine')

        driver = webdriver.PhantomJS(service_args=['--load-images=no'],
                                     executable_path=fr'{phantomjs_path}\phantomjs.exe',
                                     service_log_path='nul')
        driver.implicitly_wait(40)
        driver.set_page_load_timeout(40)

        animate('Page render engine online', end=1)

        step += 1
        login()
        step += 1
        get_subject_list()
        step += 1
        lecture_name = load_handbook()
        step += 1
        lecture_links, new_type = get_lecture_res()

        return lecture_name, lecture_links, new_type
    except KeyboardInterrupt:
        animate(end=1)
        print('Received KeyboardInterrupt!'.center(120))
        print('Quitting in 5 seconds...'.center(120))
        system('timeout 5 >nul')
        sys.exit(0)
    except:
        animate(end=1)
        print(f'An error occurred while {error_pos[step]} :('.center(120))
        from cleanup import cleanup
        cleanup()
        print('Press any key to quit.'.center(120))
        system('pause>nul')
        sys.exit(0)
