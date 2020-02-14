from os import system
from sys import _MEIPASS, exit
from time import sleep
from warnings import filterwarnings
from tempfile import gettempdir
from requests import head
from selenium import webdriver, common

from animation import animate, printProgressBar, blink

step = 0
error_pos = {1: 'login', 2: 'gathering subjects', 3: 'gathering the courseware', 4: 'getting lectures'}


def wait_to_load(element, method='id'):
    timeout = 0
    while timeout < 10:
        try:
            if method == 'id':
                driver.find_element_by_id(element)
            elif not driver.find_elements_by_tag_name(element):
                raise common.exceptions.NoSuchElementException
            break
        except common.exceptions.NoSuchElementException:
            sleep(1)
            timeout += 1


def login():
    animate('Attempting login')
    driver.get('http://122.252.249.26:96/forms/frmlogin.aspx')

    total_sum = driver.find_element_by_id('cntxt_tot_sum').get_attribute('value')
    driver.find_element_by_id('ctxt_user_id').send_keys('student')
    driver.find_element_by_id('ctxt_pass_word').send_keys('student')
    driver.find_element_by_id('cntxt_sum').send_keys(total_sum)
    driver.find_element_by_id('cmd_login').click()

    animate('Login successful!', end=1)


def get_subject_list():
    animate('Getting list of subjects')

    driver.execute_script("LoadPage('frmSubjectList.aspx',0)")
    wait_to_load('li', 'tag')

    animate('Subject list loaded!', end=1)


def load_handbook():
    animate('Gathering courseware')
    subject_list = driver.find_element_by_id('ul_subject_menu').find_elements_by_tag_name('input')
    js_functions = tuple(map(lambda x: x.get_attribute('onclick'), subject_list))
    animate('Courseware loaded!', end=1)
    for index, command in enumerate(js_functions):
        sub_name = command.split(',')[1][1:-2].split(' - ')
        sub_name = (sub_name[0] + ' ').ljust(20, '─') + ' ' + sub_name[1]

        print(f'{str(index + 1).rjust(5)}. {sub_name}')

    while True:
        try:
            cmd_no = int(input(f'Enter subject number [1-{len(js_functions)}] : ')) - 1
            if cmd_no not in range(0, len(js_functions)):
                raise ValueError
            break
        except ValueError:
            print('Wrong input! Enter again.\n')

    blink(f"Loading...{js_functions[cmd_no].split(',')[1][1:-2]}")
    global lecture_name
    lecture_name = str(cmd_no+1) + '. ' + js_functions[cmd_no].split(',')[1][1:-2]

    driver.execute_script(js_functions[cmd_no])
    wait_to_load('IFRAME_ID_1')


def get_lecture_res():
    total_lectures = len(driver.find_element_by_id('div_navigate_session').find_elements_by_tag_name('input'))
    lecture_page = driver.find_element_by_id('IFRAME_ID_1').get_attribute('src')

    driver.quit()

    lecture_page = lecture_page.split('#')[0]

    if total_lectures == 1:
        print('Lecture loaded!')
        lecture_links.append(lecture_page)
        return

    module = 1
    blink(f'{total_lectures} lectures have been found.')

    for i in range(1, total_lectures + 1):
        lecture_page = lecture_page.replace(f'_L{i - 1}', f'_L{i}')
        if head(lecture_page).status_code == 404:
            lecture_page = lecture_page.replace(f'_M{module}', f'_M{module + 1}')
            module += 1
        lecture_links.append(lecture_page)
        printProgressBar(i, total_lectures, prefix='Loading lectures', suffix='Complete', length=50)


filterwarnings('ignore')

animate('Starting page render engine')
driver = webdriver.PhantomJS(service_args=['--load-images=no'], executable_path=f'{gettempdir()}\\phantomjs.exe',
                             service_log_path=f'{_MEIPASS}\\ghostdriver.log')
animate('Page render engine online', end=1)

lecture_links = list()
lecture_name = ''

try:
    step += 1
    login()
    step += 1
    get_subject_list()
    step += 1
    load_handbook()
    step += 1
    get_lecture_res()
except:
    animate(end=1)
    print(f'An error occurred while {error_pos[step]} :(\nPress any key to exit.')
    system('PAUSE>nul')
    exit()
