#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import json
import re
import traceback
from datetime import datetime
from turtle import ht
import time

import requests


def logger(text, file="yqtb.log"):
    with open(file, "a+") as f:
        f.write(text + '\n')
        f.close()


def yqtb(username, password, name, params):
    session = requests.session()
    url = "https://yqtb.nwpu.edu.cn/wx/ry/jrsb.jsp"
    post_url = "https://yqtb.nwpu.edu.cn/wx/ry/ry_util.jsp"
    login_url = "https://uis.nwpu.edu.cn/cas/login"
    login_data = {
        # 学号
        'username': username,
        # 密码
        'password': password,
        'currentMenu': '1',
        'execution': 'e1s1',
        "_eventId": "submit"
    }
    header = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 12; M2012K11AC Build/SKQ1.211006.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/104.0.5112.97 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/29.09091)',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'https://yqtb.nwpu.edu.cn/wx/ry/jrsb_xs.jsp',
    }
    response = session.get(login_url, headers=header)
    execution = re.findall(r'name="execution" value="(.*?)"', response.text)[0]
    login_data['execution'] = execution
    response = session.post(login_url, data=login_data, headers=header)
    if "欢迎使用" in response.text:
        print(name + "login successfully")
    else:
        print(name + "login unsuccessfully")
        exit(1)
    res = ""
    for i in range(3):
        if len(res) == 0:
            response = session.get("https://yqtb.nwpu.edu.cn/wx/xg/yz-mobile/index.jsp", headers=header)
            response = session.get("https://yqtb.nwpu.edu.cn/wx/ry/jrsb.jsp", headers=header)
            pattern = r"url:'ry_util\.jsp\?sign=(.*).*'"
            res = re.findall(pattern, response.text)
    logger('res:' + str(res))
    if len(res) == 0:
        logger("error in script, please contact to the author")
        exit(1)
    time.sleep(5)
    post_url += "?sign=" + res[0]
    html = session.get(url)
    html = session.get(url, headers=header)
    time.sleep(5)
    session.headers.update({'referer': 'https://yqtb.nwpu.edu.cn/wx/ry/jrsb.jsp'})
    time.sleep(5)
    html = session.post(post_url, data=params, headers=header)
    result = '{"state":"1"}' in html.text
    #print(html.status_code)
    if result:
        logger(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + name + "信息提交成功")
    else:
        logger(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + name + "信息提交失败, HTTP错误代码: " + str(html.status_code))


def get_now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def tianbao(student_info, params):
    try:
        params['userLoginId'] = student_info[0]
        params['userName'] = student_info[2]
        yqtb(student_info[0], student_info[1], student_info[2], params)
    except:
        raise Exception(f'疫情填报运行失败\n{traceback.format_exc()}')


student_list = [
    {
        "user": ['学号', '密码', '姓名'],#[]内三项必填
        'params': {
            "hsjc": "1",
            "sfczbcqca": "",
            "czbcqcasjd": "",
            "sfczbcfhyy": "",
            "czbcfhyysjd": "",
            "actionType": "addRbxx",
            "userLoginId": "$学号",
            "userName": "$姓名",
            "szcsbm": "1",   #在学校为1，不在学校不填
            "bdzt": "1",     #在学校为1，不在学校为0
            "szcsmc": "在学校", #位置
            "szcsmc1": "在学校",  #位置
            "sfjt": "0",
            "sfjtsm": "",
            "sfjcry": "0",
            "sfjcrysm": "",
            "sfjcqz": "0",
            "sfyzz": "0",
            "sfqz": "0",
            "ycqksm": "",
            "glqk": "0",
            "glksrq": "",
            "gljsrq": "",
            "tbly": "app",
            "glyy": "",
            "qtqksm": "",
            "sfjcqzsm": "",
            "sfjkqk": "0",
            "jkqksm": "",
            "sfmtbg": "",
            "sfxn":"2",
            "sfdw":"1",
            "longlat":"108.914253,34.242023", #经纬度
            "userType": "2",
            "qrlxzt": "3",
            "xymc": "",
            "xssjhm": ""
        }
    }
]
 
def send_rtx(msg):
    webhook = r"#webhook的link"
    data = {
        'msgtype': 'text',
        'text': {
            'content': msg,
            "mentioned_mobile_list": ["@all"]
        }
    }
    res = requests.post(webhook, data=json.dumps(data))
    if res.status_code == 200:
        return True
    else:
        send_rtx(msg)


if __name__ == '__main__':
    import time
    import datetime
    while True:
        logger(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "疫情填报脚本开始运行")
        for student in student_list:
            try:
                logger(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + student.get('user')[2] + '开始填报')
                tianbao(student.get('user'), student.get('params'))
                time.sleep(30)
            except Exception as e:
                send_rtx(str(e))
        logger(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "疫情填报脚本运行结束")
        time.sleep(3600 * 6)
