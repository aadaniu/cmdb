# -*- coding: utf-8 -*-
# 2017-12-03
# by why

import smtplib, email, email.MIMEMultipart, email.MIMEBase, email.MIMEText
from email import Utils
import datetime
import os
from lib.load_config import cmdb_smtp_host,cmdb_smtp_port,cmdb_smtp_user,cmdb_smtp_password

# 依赖的smtp主机，端口，用户名，密码
smtp_host = cmdb_smtp_host
smtp_port = cmdb_smtp_port
mail_user = cmdb_smtp_user
mail_passwd = cmdb_smtp_password
# 项目目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# 获取css
def get_css():
    '''Gets  css from mail.css '''
    css = """<style type="text/css">
    <!--
    html body{font-size:12px; font-family:Tahoma, Arial, Helvetica, sans-serif;}
    .list {border:1px solid #000;width:90%;background:#D8DEEA;font-family: '微软雅黑'}
    .list td{background:#fff;padding: 5px 2px;text-align:center;vertical-align: text-top;word-break:break-all;}
    .list tr:nth-child(odd) td{background:#fff;}
    .list tr:nth-child(even) td{background:#ccc;}
    .list th{font-size:13px;height: 35px;}
    .list td{font-size:12.5px;height:20px;}
    .title {color:red;text-align:left;padding-left:5px;}
    .sql {color:blue;text-align:left;padding-left:5px;}
    .left_div{text-align:right;width:12%;float:left;}
    .right_div{text-align:left;float:left;padding-left:5px;color:green;}
    .sql_content{float:left;padding-bottom:10px;padding-top:5px;:wq;}
    .sql_detail{height:150px;padding-top: 8px;}
    -->
    </style>"""
    return css


# 列表标题
def gen_title(columns):
    title = "<tr>"
    for column in columns:
        title += "<th><h4>" + column + "</h4></th>"
    title += "</tr>"
    return title


# 内容
def gen_rows(dataSet, flag=False):
    rows = ""
    bg = ""
    for row in dataSet:
        cls = ""
        rows += "<tr %s>" % cls
        if flag:
            row_tmp = row[0:-1]
        else:
            row_tmp = row
        for e in row_tmp:
            if type(e) == unicode:
                se = e.encode('utf8')
                rows += "<td %s>" % bg + se + "</td>"
            else:
                rows += "<td %s>" % bg + str(e) + "</td>"
        rows += "</tr>"
        if flag:
            count = len(row)
            rows += "<tr><td colspan=\"%d\", color='red'>%s</td></tr>" % (count, row[-1])
    return rows


# 获取当前日期
def get_date(days):
    d = datetime.datetime.today()
    date = d - datetime.timedelta(days=days)
    return date.strftime("%Y-%m-%d")


# 发送普通邮件
def sendmail_general(femail,temail,msg):
    s = smtplib.SMTP(smtp_host, smtp_port)
    s.ehlo()        #未知
    s.starttls()    #ssl需要
    s.login(mail_user, mail_passwd)
    s.sendmail(femail, temail, msg)
    s.close()


# 发送表格邮件
# 原来的sendmail，不支持不同的表头
# def sendmail_table(subject, temail, columns, dataDict, user=None, days=0, femail=cmdb_smtp_user, flag=False):
def sendmail_table(subject, temail, dataDict, user=None, days=0, femail=cmdb_smtp_user, flag=False):
    """
        发送一个表格的邮件
    :param subject:标题
    :param temail:收件人列表(list类型)
    :param columns:表格表头(list类型)
    :param dataDict:数据(list类型)
        [
	    	{'title':'title1', 'columns':[a,b,c],'data':[[a1,b1,c1],[a2,b2,c2]},
	    	{'title':'title2', 'columns':[d,e],'data':[[d1,e1],[d2,e2]]},
        ]
    :param user:负责人
    :param days:0为今天，1为昨天。格式
    :param femail:发件人名称
    :param flag:
    :return:
        示例参考opmanage.views.test
    """
    time = get_date(days)

    message = "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">"
    message += "<html xmlns=\"http://www.w3.org/1999/xhtml\">"
    message += "<head>"
    message += "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />"
    message += "<title>Culiu</title>"

    # 原来的sendmail，不支持不同的表头
    # title = gen_title(columns)
    css = get_css()
    message += css
    if user != None:
        message += "负责人: %s <br />" % user

    # 原来的sendmail，不支持不同的表头
    # for data in dataDict:
    #     message += "<h1>%s </h1><br />" % data
    #     dataSet = dataDict[data]
    #     rows = gen_rows(dataSet, flag)
    #     message += "<table class =\"list\" >"
    #     message += title
    #     message += rows
    #     message += "</table>"

    for data in dataDict:
        message += "<h1>%s </h1><br />" % data['title']
        dataSet = data['data']
        title = gen_title(data['columns'])
        rows = gen_rows(dataSet, flag)
        message += "<table class =\"list\" >"
        message += title
        message += rows
        message += "</table>"


    message += "</body></html>"

    f = open(os.path.join(BASE_DIR, 'tmp', 'mail', subject + ".html") , "w")

    f.write(message)
    f.close()

    msg = email.MIMEText.MIMEText(message, _subtype="html", _charset="utf-8")

    msg['To'] = ",".join(temail)
    msg['From'] = femail
    msg['Subject'] = subject + ' On ' + str(time)
    msg['Date'] = Utils.formatdate(localtime=1)

    s = smtplib.SMTP(smtp_host, smtp_port)
    s.ehlo()        #未知
    s.starttls()    #ssl需要
    s.login(mail_user, mail_passwd)
    s.sendmail(femail, temail, msg.as_string())
    s.close()




