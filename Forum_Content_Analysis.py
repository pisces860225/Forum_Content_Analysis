import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from Analysis import ContentAnalysis
from threading import Thread
from juba import Similar
from random import choice
from bs4 import BeautifulSoup
import requests as rq
from queue import Queue
import jieba
import re
from NetworkArmy import proxyArmy
import time

fontName = "標楷體"
#------各 Funstion 區域--------------------------------------
class Run_Application:
    proxy = proxyArmy.getProxy(1)
    AnalysisData = ""

    def show_DISABLED(keyword_ALL):
        global startbutton
        if keyword_ALL == "  ":
            return
        else:
            startbutton['state'] = "disabled"
            count = 1
            while Run_Application.AnalysisData == "":
                if count == 11:
                    count = 1
                messagestrA = "爬找中" + ("."*count)
                startbutton['text'] = messagestrA
                count += 1
                time.sleep(1)
            startbutton['text'] = "爬找結束"
            time.sleep(1)
            startbutton['text'] = "開始爬找"
            startbutton['state'] = "active"

    def Analysis(keyword_ALL,proxy):
        global startbutton
        if keyword_ALL == "  ":
            messagebox.showinfo("警告", "關鍵字輸入欄均不可為空，請檢查")
            print("\n---------爬找結束---------")
            return
        else:
            time_start = time.time()
            SelectModalGet = SelectModalMenuA.get()
            AnalysisMode = SelectModalMenuB.get()
            print(keyword_ALL)
            Run_Application.AnalysisData = ContentAnalysis.run_Analysis(keyword_ALL,SelectModalGet,proxy,AnalysisMode)
            print(Run_Application.AnalysisData)
            time_end = time.time() #計時終止
            time_c= time_end - time_start#計算使用秒數
            print(f"\n分詞:{SelectModalGet} 分析:{AnalysisMode}\n執行時間：{time_c} 秒")
            print("\n---------爬找結束---------")
            messagebox.showinfo("搜尋成功", "花費時間為 %.2f 秒" % time_c)

    def StartCrawl():
        Run_Application.AnalysisData = ""
        keyword_ALL = rf"{KeywordInputA.get()} {KeywordInputB.get()} {KeywordInputC.get()}"
        showDISABLED = Thread(target = Run_Application.show_DISABLED,args=(keyword_ALL,))
        Analysis = Thread(target = Run_Application.Analysis,args=(keyword_ALL,Run_Application.proxy))
        showDISABLED.start()
        Analysis.start()

    def EnterKeyUp(event):
        Run_Application.StartCrawl()       

#------主 GUI 介面建構語法--------------------------------------
winMain = tk.Tk()  # 產生 TK 介面物件
winMain.geometry('755x355') # 設定視窗大小
winMain.resizable(width=0, height=0) # 是否可以改變視窗大小
winMain.title("Forum_Content_Analysis") # 視窗標題
# winMain.iconbitmap(rf'{視窗主ICON}') # 視窗 icon
# winMain.protocol("WM_DELETE_WINDOW",主系統離開)
#------主視窗選單建構語法--------------------------------------
MainMenu = tk.Menu(winMain,tearoff = 0) # 創建主視窗選單
winMain.config(menu = MainMenu) # 綁定選單於父視窗
#-------分隔線-------
MainMenuA = tk.Menu(MainMenu,tearoff = 0) # 創建 A 選項並綁定父視窗選單
MainMenuA.add_command(label = "匯出 Json 格式") # 新增 A 選單子選項
MainMenu.add_cascade(label = "檔案",menu = MainMenuA) # 命名 A 選項名稱並與該子選項綁定
#-------分隔線-------
MainMenuB = tk.Menu(MainMenu,tearoff = 0) # 創建 B 選項並綁定父視窗選單
MainMenuB.add_command(label = "Proxy 代理清單") # 新增 B 選單子選項
MainMenu.add_cascade(label = "設定",menu = MainMenuB) # 命名 B 選項名稱並與該子選項綁定
#------主視窗框架區域建構語法--------------------------------------
winMain_A = tk.LabelFrame(winMain,text="論壇清單",font=(fontName,14))
winMain_A.grid(padx=15,pady=10,ipady=21,row=0,column=0,rowspan=6)
winMain_B = tk.LabelFrame(winMain,text="搜尋設定",font=(fontName,14))
winMain_B.grid(padx=0,pady=10,ipady=5,row=0,column=1,rowspan=3)
winMain_C = tk.LabelFrame(winMain,text="模式設定",font=(fontName,14))
winMain_C.grid(padx=0,pady=0,row=3,column=1,rowspan=2)
winMain_D = tk.LabelFrame(winMain,text="操作",font=(fontName,14))
winMain_D.grid(padx=0,pady=8,ipadx=4,row=5,column=1,columnspan=2)
#------主視窗 winMain_A 框架區域論壇名稱建構語法--------------------------------------
ForumListA = tk.Label(winMain_A,anchor="w",text = "1、Dcard (狄卡)",compound='left',font=(fontName,20),width=22)
ForumListA.grid(padx=10,pady=10,row=1,column=0,columnspan=2,sticky='w')
ForumListB = tk.Label(winMain_A,anchor="w",text = "2、BabyHome",compound='left',font=(fontName,20),width=22)
ForumListB.grid(padx=10,pady=10,row=2,column=0,columnspan=2,sticky='w')
ForumListC = tk.Label(winMain_A,anchor="w",text = "3、mobile01",compound='left',font=(fontName,20),width=22)
ForumListC.grid(padx=10,pady=10,row=3,column=0,columnspan=2,sticky='w')
ForumListD = tk.Label(winMain_A,anchor="w",text = "4、巴哈姆特",compound='left',font=(fontName,20),width=22)
ForumListD.grid(padx=10,pady=10,row=4,column=0,columnspan=2,sticky='w')
ForumListE = tk.Label(winMain_A,anchor="w",text = "5、批踢踢實業坊",compound='left',font=(fontName,20),width=22)
ForumListE.grid(padx=10,pady=10,row=5,column=0,columnspan=2,sticky='w')
#------主視窗 winMain_B 框架區域查詢輸入設定建構語法--------------------------------------
KeywordTitleA = tk.Label(winMain_B,anchor="w",text = "關鍵字 A",font=(fontName,13),compound='left',width=10)
KeywordTitleA.grid(padx=10,pady=5,row=0,column=0,sticky='w')
KeywordTextA = tk.StringVar()
KeywordInputA = tk.Entry(winMain_B,relief='groove',justify='center',textvariable=KeywordTextA,bd=2,font=(fontName,13),width=25)
KeywordInputA.grid(padx=10,pady=5,row=0,column=1)
#-------分隔線-------
KeywordTitleB = tk.Label(winMain_B,anchor="w",text = "關鍵字 B",font=(fontName,13),compound='left',width=10)
KeywordTitleB.grid(padx=10,pady=5,row=1,column=0,sticky='w')
KeywordTextB = tk.StringVar()
KeywordInputB = tk.Entry(winMain_B,relief='groove',justify='center',textvariable=KeywordTextB,bd=2,font=(fontName,13),width=25)
KeywordInputB.grid(padx=10,pady=5,row=1,column=1)
#-------分隔線-------
KeywordTitleC = tk.Label(winMain_B,anchor="w",text = "關鍵字 C",font=(fontName,13),compound='left',width=10)
KeywordTitleC.grid(padx=10,pady=5,row=2,column=0,sticky='w')
KeywordTextC = tk.StringVar()
KeywordInputC = tk.Entry(winMain_B,relief='groove',justify='center',textvariable=KeywordTextC,bd=2,font=(fontName,13),width=25)
KeywordInputC.grid(padx=10,pady=5,row=2,column=1)
#------主視窗 winMain_C 框架區域模式設定建構語法--------------------------------------
SelectModalA = ["全模式","精確模式","搜尋引擎模式"]
SelectTitleA = tk.Label(winMain_C,anchor="w",text="分詞模式",font=(fontName,13),compound='left',width=10)
SelectTitleA.grid(padx=10,pady=10,row=3,column=0,sticky='w')
SelectModalMenuA = ttk.Combobox(winMain_C,justify='center',value=SelectModalA,font=(fontName,13),width=23,state='readonly')
SelectModalMenuA.grid(padx=10,pady=10,row=3,column=1)
SelectModalMenuA.current(2)
#-------分隔線-------
SelectModalB = ["詞頻模式","概率模式","詞頻逆文檔頻率模式"]
SelectTitleB = tk.Label(winMain_C,anchor="w",text="分析模式",font=(fontName,13),compound='left',width=10)
SelectTitleB.grid(padx=10,pady=0,row=4,column=0,sticky='w')
SelectModalMenuB = ttk.Combobox(winMain_C,justify='center',value=SelectModalB,font=(fontName,13),width=23,state='readonly')
SelectModalMenuB.grid(padx=10,pady=5,row=4,column=1)
SelectModalMenuB.current(1)
#------主視窗 winMain_C 框架區域啟動按鍵建構語法--------------------------------------
startbutton=tk.Button(winMain_D,text='開始爬找',font=(fontName,16),compound='left',width=30,command=Run_Application.StartCrawl)
startbutton.grid(padx=10,pady=10,row=0,column=0,columnspan=2)
#----------------------------------------------
winMain.bind('<Return>', Run_Application.EnterKeyUp)
winMain.mainloop()