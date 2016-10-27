#!/usr/bin/python
#-*- coding:utf-8 -*-

import json
import requests
import os
import smtplib
from email.mime.text import MIMEText



mail_host = 'smtp.163.com' #发件服务器

mail_user = "username"#邮箱帐户名

mail_pass = "*********" #密码

mail_postfix = '163.com' #收件服务器

mailto_list = ['clynxmac@gmail.com']


def getjson(query_params, first=True, pn=1):
    url = "http://www.lagou.com/jobs/positionAjax.json?px=default"\
          +query_params
    params = {"first": first, "pn": pn, 'kd': 'Python'}
    res = requests.post(url, params)
    return json.loads(res.text)


def parse_jobs():
    cities = [u'广州', u'深圳', u'珠海']
    ret = []
    for city in cities:
        query = u"&gx=实习&city=%s#order"%city
        res_json = getjson(query)
        results = res_json["content"]['positionResult']['result']
        for result in results:
            ret.append([result['positionName'],
                        result['salary'], 
                        result['city'],
                        result['companyShortName'],
                        result['positionId'],
                        ])
    return ret

def New_job(comp):
    '''
    对比上次抓取结果
    '''
    if not os.path.isfile('temp.txt'):
        temp_txt(comp)
        return comp
    reader = open('temp.txt', 'rb')
    lines = ''.join(reader.readlines())
    ret = []
    for com in comp:
        if '|'.join(com[:-1]).encode('utf-8') not in lines:
            ret.append(com)
    reader.close()
    return ret

def temp_txt(rows):
    '''
    保存本次抓取结果，用于下一次对比
    '''
    with open('temp.txt', 'wb') as temp:
        for row in rows:
            #不保存positionId,重新发布会改变,无参照价值
            temp.write('|'.join(row[:-1]).encode('utf-8')+'\n')


def send_mail(to_list, sub, content):
    me = "拉勾定时爬虫"+"<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEText(content, _subtype="html", _charset="utf-8")
    msg['subject'] = sub
    msg['From'] = me
    msg["To"] = ";".join(to_list)
    try:
        s = smtplib.SMTP_SSL()
        s.connect(mail_host)
        s.login(mail_user, mail_pass)
        s.sendmail(me, to_list, msg.as_string())
        s.close()
        return True

    except Exception, e:
        print str(e)
        return False
    


if __name__=='__main__':
    rows = parse_jobs()
    new = New_job(rows)
    if ret:
        content = ''
        for i in new:
            content += '|'.join(i[:-1]) +'<br>'
            content += u'链接：http://www.lagou.com/jobs/%s.html'%i[-1]
        send_mail(mailto_list, "新职位", content)
        temp_txt(rows)
