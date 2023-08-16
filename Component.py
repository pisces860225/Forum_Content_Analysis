import re
from threading import Thread
import jieba

class module():

    # 字數符號篩選器
    def character_filter(desstr, restr='',strtype = 'all'):  
        if strtype == "all":
            res = re.compile(r"[^\u4e00-\u9fa5^a-z^A-Z^]")  # 除中英文及數字外，其餘符號均去除
        elif strtype == "Eng":
            res = re.compile(r"[^\u0041-\u005a|\u0061-\u007a]+")  # 除英文大小寫外，其餘符號均去除
        elif strtype == "Num":
            res = re.compile(r"[^0-9]+")  # 除數字外，其餘符號均去除
        elif strtype == "Chn":
            res = re.compile(r"[^\u4e00-\u9fa5]+")  # 除中文外，其餘符號均去除
        return res.sub(restr, desstr)

    def Threads_join(function,args=(),ranges=30):
        threads = []
        for i in range(ranges): # range 為需要啟動多少個多執行序
            threads.append(Thread(target = function,args=args)) # 建立多執行序數據並填入多執行表單
            threads[i].start() # 多執行序起動
        for i in range(ranges):
            threads[i].join() # range 多執行序等待其他子執行序運作完成，再進行下一行程式碼

    def Disassemble(datas,choosetype):
        analyWordbox = []
        for data in datas:
            if choosetype == "全模式":
                word = jieba.cut(data,cut_all=True)
            elif choosetype == "精確模式":
                word = jieba.cut(data,cut_all=False)
            elif choosetype == "搜尋引擎模式":
                word = jieba.cut_for_search(data)
            for dat in word:
                analyWordbox.append(dat)
        return analyWordbox

    def Analysis_Mode(AnalysisMode,processdata):
        if AnalysisMode == "詞頻模式":
            AnalysisData = processdata.tf_tdm()
        elif AnalysisMode == "概率模式":
            AnalysisData = processdata.prob_tdm()
        elif AnalysisMode == "詞頻逆文檔頻率模式":
            AnalysisData = processdata.tfidf_tdm()
        return AnalysisData
        