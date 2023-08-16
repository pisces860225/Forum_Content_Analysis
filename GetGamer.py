from bs4 import BeautifulSoup
import  requests as rq
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from Component import module
from queue import Queue
from urllib import parse
from NetworkArmy import proxyArmy
import time

class GamerAnalysis():
    titleURL = Queue()
    analyzedbox = []
    analyWordbox = []
    
    def GetGamer_TitleURL(keyword):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36') 
        browser = webdriver.Chrome(r"./GoogleDrive/chromedriver.exe",chrome_options=chrome_options)
        keyurl = parse.quote(keyword)
        for page in range(1,4):
            url = fr"https://search.gamer.com.tw/?q={keyurl}#gsc.tab=0&gsc.q={keyurl}&gsc.page={page}"
            browser.get(url)
            browser.implicitly_wait(5)
            soup = BeautifulSoup(browser.page_source, 'lxml')
            urltitleData = soup.find_all(class_ = "gsc-webResult gsc-result")
            for i in urltitleData:
                GamerAnalysis.titleURL.put(i.find('a').get("data-ctorig"))
        browser.quit()

    def GetGamer():
        ichrome_options = Options()
        ichrome_options.add_argument('--headless')
        ichrome_options.add_argument('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36') 
        while True:
            try:
                iURL = GamerAnalysis.titleURL.get(False,2)
                URLnum = module.character_filter(iURL,strtype = "Num")
                URLNUM = fr"https://gnn.gamer.com.tw/ajax/gnn_list_comment.php?sn={URLnum}"
                ibrowser = webdriver.Chrome(r"./GoogleDrive/chromedriver.exe",chrome_options=ichrome_options)
                ibrowser.get(iURL)
                ibrowser.implicitly_wait(2)
                soup = BeautifulSoup(ibrowser.page_source, 'lxml')
                GamerAnalysis.analyzedbox.append(module.character_filter((soup.find("div",{"class":"GN-lbox3B"}).find("div").text),strtype = "Chn"))
                try:
                    ibrowser.get(URLNUM)
                    CommentSoup = BeautifulSoup(resp.text, 'lxml')
                    CommandData = CommentSoup.find_all("div",class_= "GN-lbox6A")
                    print(CommandData)
                    for data in CommandData:
                        GamerAnalysis.analyzedbox.append(module.character_filter((data.find("p").find('span',class_="comment-text").text),strtype = "Chn"))
                except:
                    continue
            except:
                ibrowser.quit()
                break

    def run_GetGamer(keyword,choosetype):
        GamerAnalysis.GetGamer_TitleURL(keyword)
        module.Threads_join(GamerAnalysis.GetGamer,ranges=30)
        GamerAnalysis.analyWordbox = module.Disassemble(GamerAnalysis.analyzedbox,choosetype)
        return GamerAnalysis.analyWordbox

if __name__ == '__main__':
    time_start = time.time()
    keyword = "疫情"
    choosetype = "搜尋引擎模式"
    GamerAnalysis.run_GetGamer(keyword,choosetype)
    time_end = time.time() #計時終止
    time_c= time_end - time_start#計算使用秒數
    print(f"執行時間：{time_c} 秒")
