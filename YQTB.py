import time
import requests
import tkinter as tk
from tkinter import messagebox
# 本地Chrome浏览器的静默模式设置：
from selenium import  webdriver #从selenium库中调用webdriver模块
from selenium.webdriver.chrome.options import Options # 从options模块中调用Options类
from selenium.webdriver.common.by import By
from pathlib import Path
import zipfile
import winreg
import re
import os

def original_window(): 
    enter_w = tk.Tk()
    enter_w.title('填报信息')
    enter_w.geometry('750x500')
 
    lab_1 = tk.Label(enter_w,width=7,text='用户名',compound='center')
    lab_1.place(x=200,y=200)
    
    lab_2 = tk.Label(enter_w,width=7,text='密码',compound='center')
    lab_2.place(x=200,y=230)
    global uesr_name,password
    user_name = tk.StringVar()
    password= tk.StringVar()
    ###########获取登陆账号和密码##########
    entry = tk.Entry(enter_w,textvariable=user_name) #用户名
    entry.pack()
    entry.place(x=310,y=200)
   
   
    entry_1 = tk.Entry(enter_w,show="*",textvariable=password) 
    #show使密码不可见
    entry_1.pack()
    entry_1.place(x=310,y=230)
   
 
    def panduan(a):
            tk.messagebox.showinfo('^_^','密码正确,开始填报')
            un=entry.get()#new_window(enter_w)
            pw=entry_1.get()#check_chrome_driver_update()
            a = [un,pw]
            try:
                yqtb_nwpu(a)
            except:
                get_latest_chrome_driver(get_chrome_version())
                messagebox.showinfo(title='填报结果',message='填报失败，请检查网络设置！')    
                
    btn = tk.Button(enter_w,text='登陆',fg="black",width=7,compound='center',\
                      bg = "white",command = lambda :panduan(enter_w))
    btn.pack()
    btn.place(x=330,y=270)
    enter_w.mainloop()    

# 登录按钮事件处理函数
def yqtb_nwpu(a):
    #input('请输入账号:')
    #input('请输入密码:')
    #print (a[0],a[1])
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.delete_all_cookies()
    driver.get('http://yqtb.nwpu.edu.cn/wx/xg/yz-mobile/index.jsp')#转到翱翔门户登陆页面
    time.sleep(6)

    username=driver.find_element(By.ID,'username')
    username.clear()
    username.send_keys(a[0])#抓取用户名栏并输入学号
    password=driver.find_element(By.ID,'password')
    password.clear()
    password.send_keys(a[1])#抓取密码栏并输入密码
    driver.find_element(By.NAME,'submit').click()#抓取登录按钮并点击
    time.sleep(6)

    driver.get('http://yqtb.nwpu.edu.cn/wx/ry/jrsb.jsp')
    time.sleep(6)
    
    driver.find_element(By.CLASS_NAME,'weui-btn_primary').click()#抓取提交按钮#提交
    sub2=driver.find_element(By.ID,'brcn')
    driver.execute_script("arguments[0].click();", sub2)
    driver.find_element(By.ID,'save_div').click()
    messagebox.showinfo(title='填报结果',message='填报成功！')

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
    messagebox.showinfo(title='提醒',message='请勿打开相关代理软件，否则可能闪退')
    chrome_version = get_chrome_version()
    if os.path.isfile("chromedriver.exe"):
            original_window()
    else:
        print('第一次安装正在更新相关组件')
        get_latest_chrome_driver(chrome_version)
        messagebox.showinfo(title='完成',message='更新完成，请重写打开程序')


if __name__ == '__main__':
    check_chrome_driver_update()
