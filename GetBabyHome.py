import requests as rq
from bs4 import BeautifulSoup
import queue
from urllib import parse
from Component import module
from NetworkArmy import proxyArmy

class BabyHomeAnalysis():
    urldata = queue.Queue()
    analyzedbox = []
    analyWordbox = []

    # 抓取網頁文章網址
    def GetBabyHome_TitleURL(keyword,proxy):  # keyword-關鍵字
        page = 1 # 頁數
        keyurl = parse.quote(keyword)
        for i in range(2):
            try: # 異常狀況抓取方法
                proxydata = proxyArmy.proxyUseStr(proxy)
                url=f"https://search.babyhome.com.tw/?classsort=forum&keyword={keyword}&page={page}"
                req=rq.get(url, headers={
                    "user-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
                    },proxies=proxydata)  # proxies 為塞入網路大軍參數
                if str(req.status_code) == '200':  # 網頁若回傳 200 值為正常時執行區域
                    root=BeautifulSoup(req.text,"lxml")
                    titles=root.find_all("h4", class_="media-heading")
                    for title in titles:  # 計數器
                        if page == 3:
                            break
                        link=(title.find('a',href=True))['href'].replace(keyword,keyurl) # 抓取所需網址
                        BabyHomeAnalysis.urldata.put(f"https://search.babyhome.com.tw{link}")
                    page += 1
                else: # 非 200 回傳值報錯預留區域
                    pass
            except: # 異常狀況錯誤報錯預留區域
                pass
    # 抓取網頁內文及留言
    def GetBabyhome(proxy):
        while True:
            try:
                proxydata = proxyArmy.proxyUseStr(proxy)
                url = BabyHomeAnalysis.urldata.get(False)
                req=rq.get(url, headers={
                    "user-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
                    },proxies=proxydata)
                if str(req.status_code) == '200':  # 網頁若回傳 200 值為正常時執行區域
                    root=BeautifulSoup(req.text,"lxml")
                    articles = root.find_all("div", class_="threads_content")#爬取內文與留言
                    for article in articles:
                        appStr = module.character_filter(article.text,strtype = 'Chn')
                        if appStr == "":
                            continue
                        BabyHomeAnalysis.analyzedbox.append(appStr)
                else: # 非 200 回傳值報錯預留區域
                        pass
            except:
                break

    def run_GetBabyHome(keyword,choosetype,proxy):
        BabyHomeAnalysis.GetBabyHome_TitleURL(keyword,proxy)
        module.Threads_join(BabyHomeAnalysis.GetBabyhome,args=(proxy,))
        BabyHomeAnalysis.analyWordbox = module.Disassemble(BabyHomeAnalysis.analyzedbox,choosetype)
        return BabyHomeAnalysis.analyWordbox

if __name__ == '__main__':
    keyword = "疫情"
    choosetype = "搜尋引擎模式"
    proxy = [['http', 'http://59.55.160.254:3256'], ['http', 'http://117.65.94.65:9999'], ['http', 'http://42.7.7.124:9999']]
    BabyHomeAnalysis.run_GetBabyHome(keyword,choosetype,proxy)
    print(BabyHomeAnalysis.analyWordbox) # 顯示抓取的資訊