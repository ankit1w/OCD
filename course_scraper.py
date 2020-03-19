from msvcrt import getch
from os import system
from threading import Thread
from warnings import filterwarnings

import urllib3
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException

from animation import animate, blink, printProgressBar
from path_vars import phantomjs_path

current_version = '1.0.0'

filterwarnings('ignore')
step = 0
driver = None
http = urllib3.PoolManager(timeout=10)

error_pos = ('checking for updates',
             'starting the page render engine',
             'trying to log in',
             'gathering subjects',
             'getting lectures')


def check_updates():
    global current_version
    current_version = tuple(map(int, current_version.split('.')))

    animate("Checking updates")
    update_url = 'https://raw.githubusercontent.com/ankit1w/OCD/master/latest_version'

    latest_version = http.request('GET', update_url).data[:-1].decode()
    latest_version = tuple(map(int, latest_version.split('.')))
    animate(end=1)

    if latest_version != current_version:
        print('Update available! Get the latest version from bit.ly/ocd-update'.center(120))

        if latest_version[0] > current_version[0] or latest_version[1] > current_version[1]:
            print('Press any key to launch site.'.center(120))
            getch()
            system('start https://github.com/ankit1w/OCD/releases')
            raise SystemExit(1)
        else:
            print("Press 'U' to launch update page, any other key to continue.".center(120), '\n')
            update_now = getch().decode() in ('U', 'u')

            if update_now:
                system('start https://github.com/ankit1w/OCD/releases')
                raise SystemExit(1)


def start_phantomjs():
    global driver
    animate('Starting page render engine')

    driver = webdriver.PhantomJS(service_args=['--load-images=no'],
                                 executable_path=fr'{phantomjs_path}\phantomjs.exe',
                                 service_log_path='nul')

    driver.implicitly_wait(20)
    driver.set_page_load_timeout(20)
    driver.set_script_timeout(20)

    animate('Page render engine online', end=1)


def login():
    animate('Attempting login')

    driver.execute_script("window.location.href='http://122.252.249.26:96/forms/frmlogin.aspx'")
    total_sum = driver.find_element_by_id('cntxt_tot_sum').get_attribute('value')
    driver.find_element_by_id('ctxt_user_id').send_keys('student')
    driver.find_element_by_id('ctxt_pass_word').send_keys('student')
    driver.find_element_by_id('cntxt_sum').send_keys(total_sum)
    driver.find_element_by_id('cmd_login').click()

    animate('Login successful!', end=1)


def load_handbook():
    animate('Gathering subjects')

    driver.execute_script("LoadPage('frmSubjectList.aspx',0)")

    subject_list = driver.find_element_by_id('ul_subject_menu').find_elements_by_tag_name('input')
    js_functions = tuple(map(lambda x: x.get_attribute('onclick'), subject_list))

    if not len(js_functions):
        raise

    animate('Subjects loaded!', end=1)

    for index, command in enumerate(js_functions):
        sub_name = command.split(',')[1][1:-2].split(' - ', 1)
        sub_name = (sub_name[0] + ' ').ljust(20, '─') + ' ' + sub_name[1]
        print(f'{str(index + 1).rjust(10)}. {sub_name}')

    while True:
        print()
        try:
            cmd_no = int(input(f'Enter subject number [1-{len(js_functions)}] : '.rjust(60))) - 1
            if cmd_no not in range(0, len(js_functions)):
                raise ValueError
            break
        except ValueError:
            print('Wrong input! Enter again.'.rjust(60), '\n')

    driver.execute_script(js_functions[cmd_no])
    lecture_name = js_functions[cmd_no].split(',', 1)[1][1:-2]

    system('cls')
    system('color 0f')
    system(f'title Online Courseware Downloader : Downloading ↓ {lecture_name}'.replace('&', '^&'))
    print('Online Courseware Downloader'.center(120))
    print('github.com/ankit1w/OCD'.center(120))
    print('─' * 125)
    blink(f"Loading...{lecture_name}")
    print()

    return lecture_name


def get_lecture_res():
    animate('Counting lectures')
    lecture_links = list()
    total_lectures = int(
        driver.find_element_by_id('div_navigate_session').find_elements_by_tag_name('input')[-1].get_attribute('value'))
    lecture_page = driver.find_element_by_id('IFRAME_ID_1').get_attribute('src').split('#')[0]

    phantomjs_quit = Thread(target=driver.quit)
    phantomjs_quit.start()

    if http.request('HEAD', lecture_page).status != 200:
        animate(end=1)
        print('Lecture could not be found on server.'.center(120))
        raise SystemExit

    new_type = b"src='Imagepath/" in http.request('GET', lecture_page).data

    if total_lectures == 1:
        animate('Lecture loaded!', end=1)
        lecture_links.append(lecture_page)
    else:
        module = 1
        animate(f'{total_lectures} lectures have been found.', end=1)
        print()

        for i in range(1, total_lectures + 1):
            printProgressBar(i, total_lectures, prefix=' Discovering pages', suffix='Complete', length=50)
            lecture_page = lecture_page.replace(f'_L{i - 1}', f'_L{i}')
            if http.request('HEAD', lecture_page).status == 404:
                lecture_page = lecture_page.replace(f'_M{module}', f'_M{module + 1}')
                module += 1
            lecture_links.append(lecture_page)

    return lecture_links, new_type


def course_scraper():
    global step
    try:
        check_updates()
        step = 1
        start_phantomjs()
        step = 2
        login()
        step = 3
        lecture_name = load_handbook()
        step = 4
        lecture_links, new_type = get_lecture_res()

        return lecture_name, lecture_links, new_type

    except (NoSuchElementException, urllib3.exceptions.MaxRetryError, WebDriverException):
        animate(end=1)
        print(f'An error occurred while {error_pos[step]} :('.center(120))
        print('Please check your internet connection speed and stability'.center(120))
        raise SystemExit
