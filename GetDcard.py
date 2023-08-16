import requests as rq
from bs4 import BeautifulSoup
from queue import Queue
from Component import module
from NetworkArmy import proxyArmy

class DcardAnalysis():
    titleURL = Queue()
    analyzedbox = []
    analyWordbox = []

    def GetDcard_TitleURL(keyword,proxy):
        try:
            proxydata = proxyArmy.proxyUseStr(proxy)
            url = f"https://www.dcard.tw/search/posts?query={keyword}&limit=30&after=0"
            req=rq.get(url, headers={
                "cookie":"over18=1",
                "user-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
                },proxies=proxydata)  # proxies 為塞入網路大軍參數
            if str(req.status_code) == '200':  # 網頁若回傳 200 值為正常時執行區域
                soup=BeautifulSoup(req.text,"lxml")
                aritcalroute = soup.find_all('a', {'class': 'tgn9uw-3 cUGTXH'})
                for route in aritcalroute:
                    ram = ((route.get('href')).split("/"))[-1]
                    DcardAnalysis.titleURL.put(f"https://www.dcard.tw/f/talk/p/{ram}")
            else: # 非 200 回傳值報錯預留區域
                pass
        except:
            pass
    
    def GetDcard(proxy):
        while True:
            try:
                proxydata = proxyArmy.proxyUseStr(proxy)
                url = DcardAnalysis.titleURL.get(False)
                req=rq.get(url, headers={
                    "cookie":"over18=1",
                    "user-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
                    },proxies=proxydata)
                if str(req.status_code) == '200':  # 網頁若回傳 200 值為正常時執行區域
                    soup = BeautifulSoup(req.text, 'lxml')
                    DcardAnalysis.analyzedbox.append(module.character_filter(str(soup.find('h1', {'class': 'sc-1932jlp-0 cqaWIE'}).text),strtype = 'Chn'))
                    try:
                        DcardAnalysis.analyzedbox.append(module.character_filter(soup.find( 'div', {'class': 'phqjxq-0 fQNVmg'}).text,strtype = 'Chn'))
                    except:
                        DcardAnalysis.analyzedbox.append(module.character_filter(((soup.find('div', {'class': 'xicuvi-0 fxtjxc'}).find('a', {'class': 'tgn9uw-3 cUGTXH'}).get('href')).split("/"))[-1],strtype = 'Chn'))
                else: # 非 200 回傳值報錯預留區域
                    pass
            except:
                break

    def run_GetDcard(keyword,choosetype,proxy):
        DcardAnalysis.GetDcard_TitleURL(keyword,proxy)
        module.Threads_join(DcardAnalysis.GetDcard,args=(proxy,))
        DcardAnalysis.analyWordbox = module.Disassemble(DcardAnalysis.analyzedbox,choosetype)
        return DcardAnalysis.analyWordbox

if __name__ == '__main__':
    keyword = "疫情"
    choosetype = "搜尋引擎模式"
    proxy = [['http', 'http://59.55.160.254:3256'], ['http', 'http://117.65.94.65:9999'], ['http', 'http://42.7.7.124:9999']]
    DcardAnalysis.run_GetDcard(keyword,choosetype,proxy)
    print(DcardAnalysis.analyWordbox)