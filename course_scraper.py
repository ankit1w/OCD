from os import system, _exit
from sys import _MEIPASS
from tempfile import gettempdir
from time import sleep
from warnings import filterwarnings

from requests import head, get
from selenium import common, webdriver

from animation import animate, printProgressBar, blink
from cleanup import cleanup

step = 0
driver = None
error_pos = {1: 'login', 2: 'gathering subjects', 3: 'gathering the courseware', 4: 'getting lectures'}


def check_updates():
    try:
        animate("Checking updates...")
        version = get('https://raw.githubusercontent.com/ankit1w/OCD/master/current_version').text[:-1]
        animate(end=1)
        return version
    except:
        animate('\r', end=1)
        print('An error occurred while checking for updates.\nPress any key to exit.')
        system('pause>nul')
        cleanup()
        _exit(0)


def wait_to_load(element):
    timeout = 0
    while timeout < 20:
        try:
            driver.find_element_by_id(element)
            return
        except common.exceptions.NoSuchElementException:
            sleep(0.5)
            timeout += 1

    raise common.exceptions.NoSuchElementException


def check_lecture_type(lecture_1):
    return "src='Imagepath/" in get(lecture_1).text


def login():
    animate('Attempting login')

    driver.execute_script("window.location.href='http://122.252.249.26:96/forms/frmlogin.aspx'")
    wait_to_load('cmd_login')
    total_sum = driver.find_element_by_id('cntxt_tot_sum').get_attribute('value')
    driver.find_element_by_id('ctxt_user_id').send_keys('student')
    driver.find_element_by_id('ctxt_pass_word').send_keys('student')
    driver.find_element_by_id('cntxt_sum').send_keys(total_sum)
    driver.find_element_by_id('cmd_login').click()

    animate('Login successful!', end=1)


def get_subject_list():
    animate('Getting list of subjects')

    driver.execute_script("LoadPage('frmSubjectList.aspx',0)")
    wait_to_load('ul_subject_menu')

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

    lecture_name = js_functions[cmd_no].split(',', 1)[1][1:-2]

    blink(f"Loading...{lecture_name}")

    system("title Online Courseware Downloader : "
           f"Downloading ↓ {lecture_name}".replace('&', '^&'))

    driver.execute_script(js_functions[cmd_no])
    wait_to_load('IFRAME_ID_1')

    return lecture_name


def get_lecture_res():
    lecture_links = list()
    total_lectures = len(set(map(lambda x: x.get_attribute('value'),
                                 driver.find_element_by_id('div_navigate_session').find_elements_by_tag_name('input'))))
    lecture_page = driver.find_element_by_id('IFRAME_ID_1').get_attribute('src')
    lecture_page = lecture_page.split('#')[0]

    driver.quit()

    if head(lecture_page).status_code != 200:
        print('Lecture could not be found on server.'.center(120))
        print('Press any key to exit.'.center(120))
        cleanup()
        system('pause>nul')
        _exit(0)

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
            _exit(0)

        filterwarnings('ignore')

        animate('Starting page render engine')
        try:
            driver = webdriver.PhantomJS(service_args=['--load-images=no'],
                                         executable_path=f'{gettempdir()}\\phantomjs.exe',
                                         service_log_path=f'{_MEIPASS}\\ghostdriver.log')
        except:
            pass
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
    except:
        animate(end=1)
        print(f'An error occurred while {error_pos[step]} :('.center(120))
        print('Press any key to exit.'.center(120))
        system('pause>nul')
        driver.quit()
        from cleanup import cleanup
        cleanup()
        _exit(0)
