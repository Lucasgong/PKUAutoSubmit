import copy
import json
import os
import sys
import time
from argparse import ArgumentParser
from urllib import request
from urllib.parse import quote

from selenium import webdriver
from selenium.webdriver import Chrome, Firefox, PhantomJS
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

#from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from urllib.parse import quote
from urllib import request
import time
import warnings
import json
warnings.filterwarnings('ignore')


def login(driver, userName, password, retry=0):
    if retry == 3:
        raise Exception('门户登录失败')

    print('门户登陆中...')

    appID = 'portal2017'
    iaaaUrl = 'https://iaaa.pku.edu.cn/iaaa/oauth.jsp'
    appName = quote('北京大学校内信息门户新版')
    redirectUrl = 'https://portal.pku.edu.cn/portal2017/ssoLogin.do'

    driver.get('https://portal.pku.edu.cn/portal2017/')
    driver.get(
        f'{iaaaUrl}?appID={appID}&appName={appName}&redirectUrl={redirectUrl}')
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, 'logon_button')))
    driver.find_element_by_id('user_name').send_keys(userName)
    time.sleep(0.1)
    driver.find_element_by_id('password').send_keys(password)
    time.sleep(0.1)
    driver.find_element_by_id('logon_button').click()
    try:
        WebDriverWait(driver,
                      5).until(EC.visibility_of_element_located((By.ID, 'all')))
        print('门户登录成功！')
    except:
        print('Retrying...')
        login(driver, userName, password, retry + 1)


def go_to_simso(driver):
    driver.find_element_by_id('all').click()
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, 'tag_s_stuCampusExEnReq')))
    driver.find_element_by_id('tag_s_stuCampusExEnReq').click()
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[-1])
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'el-card__body')))


def go_to_application_out(driver):
    go_to_simso(driver)
    driver.find_element_by_class_name('el-card__body').click()
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'el-select')))


def go_to_application_in(driver, userName, password):
    driver.back()
    driver.back()
    try:
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'el-card__body')))
        time.sleep(0.5)
        driver.find_element_by_class_name('el-card__body').click()
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'el-select')))
    except:
        print('检测到会话失效，重新登陆中...')
        login(driver, userName, password)
        go_to_simso(driver)
        driver.find_element_by_class_name('el-card__body').click()
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'el-select')))


def select_in_out(driver, way):
    driver.find_element_by_class_name('el-select').click()
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located(
            (By.XPATH, f'//li/span[text()="{way}"]')))
    driver.find_element_by_xpath(f'//li/span[text()="{way}"]').click()


def select_campus(driver, campus):
    driver.find_elements_by_class_name('el-select')[1].click()
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located(
            (By.XPATH, f'//li/span[text()="{campus}"]')))
    driver.find_element_by_xpath(f'//li/span[text()="{campus}"]').click()


def select_destination(driver, destination):
    driver.find_elements_by_class_name('el-select')[2].click()
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located(
            (By.XPATH, f'//li/span[text()="{destination}"]')))
    driver.find_element_by_xpath(f'//li/span[text()="{destination}"]').click()


def select_district(driver, district):
    driver.find_elements_by_class_name('el-select')[3].click()
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located(
            (By.XPATH, f'//li/span[text()="{district}"]')))
    driver.find_element_by_xpath(f'//li/span[text()="{district}"]').click()


def write_reason(driver, reason):
    driver.find_element_by_class_name('el-textarea__inner').send_keys(
        f'{reason}')
    time.sleep(0.1)


def write_track(driver, track):
    driver.find_elements_by_class_name('el-textarea__inner')[1].send_keys(
        f'{track}')
    time.sleep(0.1)


def write_street(driver, street):
    driver.find_elements_by_class_name('el-textarea__inner')[1].send_keys(
        f'{street}')
    time.sleep(0.1)


def click_check(driver):
    driver.find_element_by_class_name('el-checkbox__label').click()
    time.sleep(0.1)


def click_inPeking(driver):
    driver.find_element_by_class_name('el-radio__inner').click()
    time.sleep(0.1)


def submit(driver):
    driver.find_element_by_xpath('//button/span[contains(text(),"保存")]').click()
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located(
            (By.XPATH, '(//button/span[contains(text(),"提交")])[3]')))
    driver.find_element_by_xpath(
        '(//button/span[contains(text(),"提交")])[3]').click()
    time.sleep(0.1)


def fill_out(driver, campus, reason, destination, track):
    print('开始填报出校备案')

    print('选择出校/入校    ', end='')
    select_in_out(driver, '出校')
    print('Done')

    print('选择校区    ', end='')
    select_campus(driver, campus)
    print('Done')

    print('填写出入校事由    ', end='')
    write_reason(driver, reason)
    print('Done')

    print('选择出校目的地    ', end='')
    select_destination(driver, destination)
    print('Done')

    print('填写出校行动轨迹    ', end='')
    write_track(driver, track)
    print('Done')

    click_check(driver)
    submit(driver)

    print('出校备案填报完毕！')


def fill_in(driver, campus, reason, habitation, district, street):
    print('开始填报入校备案')

    print('选择出校/入校    ', end='')
    select_in_out(driver, '入校')
    print('Done')

    print('填写出入校事由    ', end='')
    write_reason(driver, reason)
    print('Done')

    if habitation != '北京':
        raise Exception('暂不支持京外入校备案，请手动填写')

    print('选择居住地所在区    ', end='')
    select_district(driver, district)
    print('Done')

    print('填写居住地所在街道    ', end='')
    write_street(driver, street)
    print('Done')

    click_inPeking(driver)
    click_check(driver)
    submit(driver)

    print('入校备案填报完毕！')


def screen_capture(driver, path):
    driver.back()
    driver.back()
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'el-card__body')))
    driver.find_elements_by_class_name('el-card__body')[1].click()
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located(
            (By.XPATH, '//button/span[contains(text(),"加载更多")]')))
    driver.maximize_window()
    time.sleep(0.1)
    driver.save_screenshot(path + 'result.png')
    print('备案历史截图已保存')


def wechat_notification(userName, sckey):
    with request.urlopen(
            quote('https://sc.ftqq.com/' + sckey + '.send?text=成功报备&desp=学号' +
                  str(userName) + '成功报备',
                  safe='/:?=&')) as response:
        response = json.loads(response.read().decode('utf-8'))
    if response['errmsg'] == 'success':
        print('微信通知成功！')
    else:
        print(str(response['errno']) + ' error: ' + response['errmsg'])


def run(driver, userName, password, campus, reason, destination, track,
        habitation, district, street, sckey):
    login(driver, userName, password)
    print('=================================')

    go_to_application_out(driver)
    fill_out(driver, campus, reason, destination, track)
    print('=================================')

    go_to_application_in(driver, userName, password)
    fill_in(driver, campus, reason, habitation, district, street)
    print('=================================')

    if sckey != '0':
        wechat_notification(username, sckey)
        print('=================================')

    print('可以愉快的玩耍啦！')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--username', '-u', type=str, help='用户名', default='1')
    parser.add_argument('--password', '-p', type=str, help='密码', default='1')
    parser.add_argument('--campus', type=str,
                        help='出发点, 燕园、万柳、畅春园、圆明园、中关新园', default='燕园')
    parser.add_argument('--reason', type=str,
                        help='出校原因, eg. 吃饭', default='万柳')
    parser.add_argument('--destination', type=str,
                        help='出校目的地, eg. 北京', default='北京')
    parser.add_argument('--track', type=str,
                        help='出校轨迹, eg. 畅春园食堂', default='万柳')
    parser.add_argument('--habitation', type=str,
                        help='入校前居住地, eg. 北京', default='北京')
    parser.add_argument('--district', type=str,
                        help='入校前居住所在区, eg. 海淀区', default='海淀区')
    parser.add_argument('--street', type=str,
                        help='入校前居住所在街道, eg. 燕园街道', default='万柳街道')
    parser.add_argument('--sckey', '-s', type=str,
                        help='wechat sckey', default='0')
    args = parser.parse_args()

    args_public = copy.deepcopy(args)
    args_public.password = 'xxxxxxxx'
    print('Arguments: {}'.format(args_public))
    print('Driver Launching...')

    #driver = Firefox()
    #driver = webdriver.Chrome(ChromeDriverManager().install())

    if sys.platform == 'darwin':  # macOS
        phantomjs_path = os.path.join('phantomjs', 'phantomjs-darwin')
    elif sys.platform == 'linux':  # linux
        phantomjs_path = os.path.join('phantomjs', 'phantomjs-linux-x86_64')
    else:  # windows
        phantomjs_path = os.path.join('phantomjs', 'phantomjs-windows.exe')

    driver = PhantomJS(executable_path=phantomjs_path,service_args=['--ignore-ssl-errors=true','--ssl-protocol=TLSv1'])

    run(driver, args.username, args.password, args.campus, args.reason, args.destination, args.track,
        args.habitation, args.district, args.street, args.sckey)
    
    driver.quit()
    
