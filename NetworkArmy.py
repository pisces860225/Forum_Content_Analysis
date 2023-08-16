import requests as rq
from bs4 import BeautifulSoup
from time import sleep
from queue import Queue
from threading import Thread
from Component import module
from random import choice

class proxyArmy:
    proxydata = Queue()
    returnfile = []

    def proxyStr(data_type,proxy_ip,proxy_port):  # proxy驗證字串組裝
        proxy = {
                    f"{data_type}": f"{data_type}://{proxy_ip}:{proxy_port}"
                }
        return proxy
    def proxyUseStr(returnfile):  # proxy驗證字串組裝
        ChoiceData = choice(returnfile)
        proxy = {
                    f"{ChoiceData[0]}": f"{ChoiceData[1]}"
                }
        return proxy

    def proxyreturnStr(data_type,proxy_ip,proxy_port):  # proxy字串組裝
        proxy_url = f"{data_type}://{proxy_ip}:{proxy_port}"
        return proxy_url

    def checkIP():
        while True:
            try:
                data = proxyArmy.proxydata.get(False)
                proxy = proxyArmy.proxyStr(data[2],data[0],data[1]) # proxy字串組裝運用
                url = 'https://www.google.com.tw/'
                resp = rq.get(url, proxies=proxy, timeout=2)
                if str(resp.status_code) == '200':
                    proxy_return = proxyArmy.proxyreturnStr(data[2],data[0],data[1])
                    proxyArmy.returnfile.append([data[2],proxy_return])
                else:
                    pass
            except:
                break

    def getProxy(pages):  # x 為想要抓取網頁的頁數
        for i in range(1, pages+1):
            url = f"https://www.kuaidaili.com/free/inha/{i}/"
            aritcalres = rq.get(url, timeout=3)
            aritcalsoup = BeautifulSoup(aritcalres.text, 'html.parser')
            tableData = aritcalsoup.find('div', {'id': 'list'}).find('table', {'class': 'table table-bordered table-striped'}).find('tbody').find_all('tr') # 網頁提供資料表格定位
            # 開始抓取個別所需資料
            for data in tableData:  
                ip = str(data.find('td', {'data-title': 'IP'}).text)
                port = data.find('td', {'data-title': 'PORT'}).text
                urltype = data.find('td', {'data-title': '类型'}).text.lower() # 請求型態抓取並轉換為小寫字母
                proxyArmy.proxydata.put([ip,port,urltype])
            sleep(0.8)  # 小睡一會，低於此數將會回報錯誤
        module.Threads_join(proxyArmy.checkIP,ranges=15)
        return proxyArmy.returnfile

if __name__ == '__main__':
    data = proxyArmy.getProxy(1)
    # print(data)
    print(proxyArmy.proxyUseStr(data))
    