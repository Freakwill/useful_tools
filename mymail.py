# -*- coding: utf-8 -*-
'''
send email
'''
import smtplib
from email.mime.text import MIMEText
# from email.header import Header

# server, username, postfix, password
# 'host':'smtp.163.com'
# 'user':'songcwzjut'

mymail={'126':'songcongwei1986@126.com','163':'songcwzjut@163.com',\
        'sina':'songcongwei54@sina.com'}

mymail163={'host':'smtp.163.com',\
     'user':'songcwzjut@163.com',\
     'password':'19860705',\
     'name': 'William<%s>' % mymail['163']}

mymail126={'host':'smtp.126.com',\
     'user':'songcongwei1986@126.com',\
     'password':'19860705',\
     'name': 'William<%s>' % mymail['126']}

mymailsina={'host':'smtp.sina.com.cn',\
     'user':'songcongwei54@sina.com',\
     'password':'19190504',\
     'name': 'William<%s>' % mymail['sina']}


from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.utils import COMMASPACE,formatdate
from email import encoders

import os

def send_mail(mail,to_list,subject,content):
    '''
mailto_list=('songcwzjut@163.com','281124072@qq.com')
try:
    send_mail(mymail126,mailto_list,"making love","fucking me \
             \n I will fuck your mother, son of bitch.\n go to www.baidu.com")
    print("success")
except Exception as ex:
    print(ex)
    '''
    if files:
        msg = MIMEMultipart()
        msg['From'] = mail['name']
        msg['Subject'] = subject
        msg['To'] = COMMASPACE.join(to) # COMMASPACE==', '
        msg['Date'] = formatdate(localtime=True)
        msg.attach(MIMEText(text))

        if not isinstance(files,(list,tuple)):
            files=[files]
        for file in files:
            part = MIMEBase('application', 'octet-stream') #'octet-stream': binary data
            part.set_payload(open(file, 'rb').read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"'\
                            % os.path.basename(file))
            # att = MIMEText(open('h:\\python\\1.jpg', 'rb').read(), 'base64', 'utf-8')
            # att["Content-Type"] = 'application/octet-stream'
            # att["Content-Disposition"] = 'attachment; filename="1.jpg"'
            msg.attach(part)
    else:
        msg = MIMEText(content,_subtype='plain',_charset='gb2312')
        # MIMEText('content','text','utf-8')
        # you need 'utf-8' for Chinese and other languages
        msg['Subject'] = subject # Header(subject, 'utf-8')
        msg['From'] = mail['name']
        msg['To'] = ";".join(to_list)

    serv = smtplib.SMTP(mail['host'])    #server.connect(mail['host'])
    serv.login(mail['user'], mail['password'])
    serv.sendmail(mail['name'], to, msg.as_string())
    serv.close()


# password crack
def bruteforce(mail,pwdict):
    for pw in pwdict:
        server = smtplib.SMTP()
        server.connect(mail['host'])
        try:
            server.login(mail['user'],pw)
            print('%s is the password of %s'%(pw,mail['user']))
            server.close()
        except:
            pass
    server.close()