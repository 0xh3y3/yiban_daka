#!/usr/bin/env python
# coding:utf-8
import requests
import base64
import json
import time
import smtplib
import random
from bs4 import BeautifulSoup
from email.mime.text import MIMEText


# proxy代理抓包
# proxies={'http':'http://127.0.0.1:8080','https':'https://127.0.0.1:8080'}

def loginCookies(username, password):
    url = "http://202.203.16.42/"
    path = "/login/Login.htm"
    data = {
        "username": base64.b64encode(username.encode()).decode(),
        "password": base64.b64encode(password.encode()).decode(),
    }
    session.post(url=url + path, headers=headers, data=data)
    html = (session.get(url="http://202.203.16.42/user/index.htm", headers=headers)).text
    name = (
        (BeautifulSoup(html, features="html.parser")).find("span", class_="header-content-personal-name")).text.strip()
    return name


def part(time_i):
    data = {
        # "data": json.dumps({"xmqkb": {"id":time_i}, "pdnf": "2020", "type": "xsfxtwjc", "c1": "小于37.3°C","c2": "否"},separators=(',', ':')),
        # "data": json.dumps({"xmqkb":{"id":time_i},"pdnf":"2020","type":"xsfxtwjc","c1":"小于37.3℃","c2":"否"},separators=(',', ':')),
        "data": json.dumps({"xmqkb": {"id": time_i}, "pdnf": "2020", "type": "xsfxtwjc", "c1": "小于37.3℃", "c2": "否"},
                           separators=(',', ':')),
        "msgUrl": "syt/zzglappro/index.htm?type=xsfxtwjc&xmid=4a4b90aa73faf66a0174116ae01b0a14",
        "multiSelectData": ""
    }
    res = (session.post(url="http://202.203.16.42/syt/zzapply/operation.htm", data=data, headers=headers)).text
    return res


def DK():
    if "05:00:00" <= now_localtime < "12:00:00":
        return part(timelist[0])
    elif "12:00:00" <= now_localtime < "22:00:00":
        return part(timelist[1])


# 163邮箱发送邮件(有验证码用服务器处理更方便)
def SmtpSpend():
    # 邮件构建
    subject = "打卡日志"  # 邮件标题
    f = open('DKresult_list.txt', 'r')
    content = f.read()
    f.close()
    sender = ""  # 发送方
    recver = ""  # 接收方
    password = ""  # 邮箱密码
    message = MIMEText(content, "plain", "utf-8")  # content 发送内容     "plain"文本格式   utf-8 编码格式
    message['Subject'] = subject  # 邮件标题
    message['To'] = recver  # 收件人
    message['From'] = sender  # 发件人
    smtp = smtplib.SMTP_SSL("smtp.163.com", 465)  # 实例化smtp服务器
    smtp.login(sender, password)  # 发件人登录
    smtp.sendmail(sender, [recver], message.as_string())  # as_string 对 message 的消息进行了封装
    smtp.close()


if __name__ == '__main__':
    start_time = time.time()
    username = (open("Username_list.txt", 'r').read().splitlines())
    password = (open("Password_list.txt", 'r').read().splitlines())
    timelist = ["ff8080817f8b5c9e017fdf5314b13a7e", "ff8080817f8b5da8017fdf53e9af3ac3"]
    captcahurl = 'http://202.203.16.42:80/nonlogin/login/captcha/isvalid.htm'
    session = requests.Session()
    now_localtime = time.strftime("%H:%M:%S", time.localtime())  # 获取当前时间
    while True:
        try:
            for i in range(len(username)):
                result = (session.get(url=captcahurl)).text
                if result == "false":
                    headers = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.50"}
                    name = loginCookies(username[i], password[i])
                    while True:
                        res = str(DK())
                        print(res)
                        if res == "Applied today" or res == "success":
                            DKresult = name + " " + username[i] + " " + res
                            DKresultfile = open("DKresult_list.txt", 'a', newline="")
                            DKresultfile.write(DKresult + "\n")
                            DKresultfile.close()
                            print(DKresult)
                            break
                        else:
                            continue
                else:
                    while True:
                        proxy = str(random.randint(1, 255)) + "." + str(random.randint(1, 255)) + "." + str(
                            random.randint(1, 255)) + "." + str(random.randint(1, 255))
                        headers = {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.50",
                            "X-Forwarded-For": proxy
                        }
                        result = (session.get(url=captcahurl, headers=headers)).text
                        if result == "false":
                            name = loginCookies(username[i], password[i])
                            while True:
                                res = str(DK())
                                if res == "Applied today" or res == "success":
                                    DKresult = name + " " + username[i] + " " + res
                                    DKresultfile = open("DKresult_list.txt", 'a', newline="")
                                    DKresultfile.write(DKresult + "\n")
                                    DKresultfile.close()
                                    print(DKresult)
                                    break
                                else:
                                    continue
                            break
                        else:
                            continue
            break
        except:
            time.sleep(3)
    now_localtime_NYR = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 获取当前时间
    renshu = len(username)
    end_time = time.time()
    spend_time_min = (str((end_time - start_time)/60)).split('.')[0]
    spend_time_s = (str((end_time - start_time)%60)).split('.')[0]
    f = open("DKresult_list.txt", 'a', newline="")
    f.write("截至到    " + now_localtime_NYR + "\n" + "完成打卡人数为:" + str(renshu) + "人" + "  共用时:" + spend_time_min + "分" + spend_time_s + "秒")
    f.close()
    SmtpSpend()
    f = open('DKresult_list.txt', 'a+')
    f.truncate(0)  # 清空打卡记录
    f.close()
