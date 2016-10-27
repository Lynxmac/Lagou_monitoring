#!/usr/bin/python
#-*- coding:utf-8 -*-

import json
import requests
import os
import smtplib
from email.mime.text import MIMEText


API_KEY = ''


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
        if '|'.join(com[:-1]).encode('utf-8') in lines:
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


def ifttt_trigger(value1=None, value2=None, value3=None):
    URL = 'https://maker.ifttt.com/trigger/{event}/with/key/{key}'.format(event='send', key=API_KEY)
    DATA = {'value1': value1, 'value2': value2, 'value3': value3}
    res = requests.post(url=URL, data=DATA)
    print res.status_code
    


if __name__=='__main__':
    rows = parse_jobs()
    new = New_job(rows)
    if new:
        content = ''
        for i in new:
            content += '|'.join(i[:-1]) + '<br>'
            content += "<a href='http://www.lagou.com/jobs/%s.html'>"%i[-1] + u'链接</a><br>'
        ifttt_trigger(content)
        temp_txt(rows)
