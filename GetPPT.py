import requests as rq
from bs4 import BeautifulSoup
from queue import Queue
from Component import module
from NetworkArmy import proxyArmy

class PttAnalysis():
    urldata = Queue()
    analyzedbox = []
    analyWordbox = []

    # 抓取網頁文章網址
    def GetPPT_TitleURL(keyword,proxy):  # keyword-關鍵字  proxy-網路大軍
        page = 1 # 頁數
        for i in range(2):
            try: # 異常狀況抓取方法
                proxydata = proxyArmy.proxyUseStr(proxy)
                url=f"https://www.ptt.cc/bbs/Gossiping/search?page={page}&q={keyword}"
                req=rq.get(url, headers={
                    "cookie":"over18=1",
                    "user-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
                    },proxies=proxydata)  # proxies 為塞入網路大軍參數
                if str(req.status_code) == '200':  # 網頁若回傳 200 值為正常時執行區域
                    root=BeautifulSoup(req.text,"lxml")
                    titles=root.find_all("div",class_="title")
                    register = 0
                    for title in titles:  # 計數器
                        if page == 2:
                            if register == 10:
                                break
                        link=title.find('a',href=True) # 抓取所需網址
                        PttAnalysis.urldata.put(f"https://www.ptt.cc{link['href']}")
                        register += 1
                    page += 1
                else: # 非 200 回傳值報錯預留區域
                    pass
            except: # 異常狀況錯誤報錯預留區域
                pass

    # 抓取網頁內文及留言
    def GetPPT(proxy):
        while True:
            try:
                proxydata = proxyArmy.proxyUseStr(proxy)
                url = PttAnalysis.urldata.get(False)
                req=rq.get(url, headers={
                    "cookie":"over18=1",
                    "user-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
                    },proxies=proxydata)
                if str(req.status_code) == '200':  # 網頁若回傳 200 值為正常時執行區域
                    root=BeautifulSoup(req.text,"lxml")
                    main_container = root.find(id='main-container')  #爬取內文
                    if main_container == None:
                        continue
                    PttAnalysis.analyzedbox.append(module.character_filter(main_container.text,strtype = 'Chn'))
                    
                    articles = root.find_all('div', 'push')#爬取留言
                    for article in articles:
                        PttAnalysis.analyzedbox.append(module.character_filter(article.find('span','f3 push-content').getText(),strtype = 'Chn'))

                else: # 非 200 回傳值報錯預留區域
                        pass
            except:
                break

    def run_GetPtt(keyword,choosetype,proxy):
        PttAnalysis.GetPPT_TitleURL(keyword,proxy)
        module.Threads_join(PttAnalysis.GetPPT,args=(proxy,))
        PttAnalysis.analyWordbox = module.Disassemble(PttAnalysis.analyzedbox,choosetype)
        return PttAnalysis.analyWordbox
 
if __name__=="__main__":
    keyword = "疫情"
    choosetype = "搜尋引擎模式"
    proxy = [['http', 'http://59.55.160.254:3256'], ['http', 'http://117.65.94.65:9999'], ['http', 'http://42.7.7.124:9999']]
    PttAnalysis.run_GetPtt(keyword,choosetype,proxy)
    print(PttAnalysis.analyWordbox) # 顯示抓取的資訊