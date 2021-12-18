import time
import requests
from tkinter import messagebox
# 本地Chrome浏览器的静默模式设置：
from selenium import  webdriver #从selenium库中调用webdriver模块
from selenium.webdriver.chrome.options import Options # 从options模块中调用Options类
from pathlib import Path
import zipfile
import winreg
import re
import os

def yqtb_nwpu():
    un=input("请输入学号:")
    pw=input("请输入密码:")
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.delete_all_cookies()
    driver.get('http://yqtb.nwpu.edu.cn/wx/xg/yz-mobile/index.jsp')#转到翱翔门户登陆页面
    time.sleep(6)

    username=driver.find_element_by_id('username')
    username.clear()
    username.send_keys(un)#抓取用户名栏并输入学号
    password=driver.find_element_by_id('password')
    password.clear()
    password.send_keys(pw)#抓取密码栏并输入密码
    driver.find_element_by_name('submit').click()#抓取登录按钮并点击
    time.sleep(6)

    driver.get('http://yqtb.nwpu.edu.cn/wx/ry/jrsb.jsp')
    time.sleep(6)
    
    driver.find_element_by_class_name('weui-btn_primary').click()#抓取提交按钮#提交
    sub2=driver.find_element_by_id('brcn')
    driver.execute_script("arguments[0].click();", sub2)
    driver.find_element_by_id('save_div').click()

python_root = os.path.abspath('.')  # .py当前目录
base_url = 'http://npm.taobao.org/mirrors/chromedriver/'  # chromedriver在国内的镜像网站
version_re = re.compile(r'^[1-9]\d*\.\d*.\d*')  # 匹配前3位版本信息

def download(link, file_name):
    response = requests.get(link)
    file = response.content
    with open(file_name, 'wb') as f:
        f.write(file)
def unzip(zip_file):
    extracting = zipfile.ZipFile(zip_file)
    extracting.extractall('.')
    extracting.close()
    os.remove(zip_file)
    
def get_chrome_version():
    """通过注册表查询Chrome版本信息: HKEY_CURRENT_USER\SOFTWARE\Google\Chrome\BLBeacon: version"""
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'SOFTWARE\Google\Chrome\BLBeacon')
        value = winreg.QueryValueEx(key, 'version')[0]
        return version_re.findall(value)[0]
    except WindowsError as e:
        return '0.0.0'  # 没有安装Chrome浏览器


def get_chrome_driver_version():
    try:
        result = os.popen('chromedriver --version').read()
        version = result.split(' ')[1]
        return '.'.join(version.split('.')[:-1])
    except Exception as e:
        return '0.0.0'  # 没有安装ChromeDriver


def get_latest_chrome_driver(chrome_version):
    url = f'{base_url}LATEST_RELEASE_{chrome_version}'
    latest_version = requests.get(url).text
    download_url = f'{base_url}{latest_version}/chromedriver_win32.zip'
    if os.path.exists('chromedriver.exe'):
        os.remove('chromedriver.exe')
    download(download_url, 'chromedriver.zip')
    unzip('chromedriver.zip')
    return True


def check_chrome_driver_update():
    chrome_version = get_chrome_version()
    driver_version = get_chrome_driver_version()
    if chrome_version == driver_version:
        print('No need to update')
    else:
        try:
            get_latest_chrome_driver(chrome_version)
        except Exception as e:
            print(f'Fail to update: {e}')


if __name__ == '__main__':
    check_chrome_driver_update()

try:
    yqtb_nwpu()
    messagebox.showinfo(title='填报结果',message='填报成功')
except:
    messagebox.showinfo(title='填报结果',message='填报失败')
