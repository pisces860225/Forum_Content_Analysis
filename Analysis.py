from juba import Similar
from threading import Thread
from Component import module
from GetPPT import PttAnalysis
from GetDcard import DcardAnalysis
from GetBabyHome import BabyHomeAnalysis
from GetGamer import GamerAnalysis

class ContentAnalysis:
    def catch_PttContent(keyword,choosetype,proxy):
        ContentAnalysis.AllContent.append(PttAnalysis.run_GetPtt(keyword,choosetype,proxy))
    def catch_DcardContent(keyword,choosetype,proxy):
        ContentAnalysis.AllContent.append(DcardAnalysis.run_GetDcard(keyword,choosetype,proxy))
    def catch_GamerContent(keyword,choosetype):
        ContentAnalysis.AllContent.append(GamerAnalysis.run_GetGamer(keyword,choosetype))
    def catch_BabyHomeContent(keyword,choosetype,proxy):
        ContentAnalysis.AllContent.append(BabyHomeAnalysis.run_GetBabyHome(keyword,choosetype,proxy))
    # def catch_Mobile01Content(keyword,choosetype,proxy):
    #     ContentAnalysis.AllContent.append(Mobile01Analysis.run_GetMobile01(keyword,choosetype,proxy))

    def catch_allContent(keyword,choosetype,proxy):
        GetPtt = Thread(target = ContentAnalysis.catch_PttContent,args=(keyword,choosetype,proxy))
        GetDcard = Thread(target = ContentAnalysis.catch_DcardContent,args=(keyword,choosetype,proxy))
        GetGamer = Thread(target = ContentAnalysis.catch_GamerContent,args=(keyword,choosetype))
        GetBabyHome = Thread(target = ContentAnalysis.catch_BabyHomeContent,args=(keyword,choosetype,proxy))
        # GetMobile01 = Thread(target = ContentAnalysis.catch_Mobile01Content,args=(keyword,choosetype,proxy))

        GetPtt.start()
        GetDcard.start()
        GetGamer.start()
        GetBabyHome.start()
        # GetMobile01.start()0

        GetPtt.join()
        GetDcard.join()
        GetGamer.join()
        GetBabyHome.join()
        # GetMobile01.join()

    def run_Analysis(keyword,choosetype,proxy,AnalysisMode):
        ContentAnalysis.AllContent = []
        ContentAnalysis.catch_allContent(keyword,choosetype,proxy)
        processdata = Similar(ContentAnalysis.AllContent)
        AnalysisData = module.Analysis_Mode(AnalysisMode,processdata)
        return AnalysisData       

if __name__ == '__main__':
    import pandas as pd
    keyword = "疫情"
    choosetype = "搜尋引擎模式"
    AnalysisMode = "概率模式"
    proxy = [['http', 'http://59.55.160.254:3256'], ['http', 'http://117.65.94.65:9999'], ['http', 'http://42.7.7.124:9999']]
    processdata = ContentAnalysis.run_Analysis(keyword,choosetype,proxy,AnalysisMode)
    print(processdata)