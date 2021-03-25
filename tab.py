# ---------------------------------------------------------
# 視窗畫面2
import tkinter as tk
from tkinter import ttk
import pandas as pd
from mojim import __init__ as moj
from Bayes import __init__ as bay
from person import __init__ as per
import threading # 子執行緒


win = tk.Tk()
win.title("下載視窗")
win.geometry("400x400")

nb = ttk.Notebook(win)
tab1 = tk.Frame(nb)

nb.add(tab1, text="下載歌詞")
nb.pack()

tab2 = tk.Frame(nb)
nb.add(tab2, text="分析")
nb.pack()

tab3 = tk.Frame(nb)
nb.add(tab3, text="圖表化")
nb.pack()

# ---------------------------------------------------- tab1

label1 = tk.Label(tab1, text="2020華語歌手排行前五位")
label1.pack()

label2 = tk.Label(tab1, text="周杰倫、鄧紫棋、五月天、周興哲、陳奕迅")
label2.pack()

# ---------------------------------------------------- 創進度條
p1 = ttk.Progressbar(tab1,length=200,cursor='spider',
                     mode="determinate",
                     orient=tk.HORIZONTAL)
p1.pack(padx=10, pady=20)
p1["value"] = 0
p1["maximum"] = 200
# ----------------------------------------------------
def thr1():
    inp =["周杰倫","鄧紫棋","林俊傑","周興哲","陳奕迅"]
    # inp = ["陳奕迅"]
    l = 0
    for i in inp:
        m = moj(i)
        l += 40
        p1["value"] = l
        df = pd.DataFrame(m)
        df.to_csv("{}.csv".format("2020華語歌手排行前五位"), encoding="utf-8", index=False)
        p1.update()


def thr():
    # 设置线程为守护线程，防止退出主线程时，子线程仍在运行
    t.setDaemon(True)
    t.start()

# ----------------------------------------------------
t = threading.Thread(target=thr1)

button1 = tk.Button(tab1, text="下載", pady=5, command=thr)
button1.pack()

# ---------------------------------------------------- tab2

def but():
    if t.is_alive() == True:
        t.join()
    label2 = tk.Label(tab2, text=bay(entry1.get()))
    label2.pack()
    print(label2)
    # print(bay(entry1.get()))

    # label3 = tk.Label(tab2, text=bay_print,padx=100, pady=100, bg="#777")
    # label3.pack()

entry1 = tk.Entry(tab2, width="350",)
entry1.pack()

button2 = tk.Button(tab2, text="分析", pady=5, command=but)
button2.pack()

# ---------------------------------------------------- tab3

def peron():
    bay_print = bay(entry1.get())
    if bay_print != None:
        per(bay_print)

button3 = tk.Button(tab3, text="圖表化", pady=5, command=peron)
button3.pack()

# ----------------------------------------------------
win.mainloop()

# ----------------------------------------------------

# 問題1 : 能不能推斷出哪一首歌 A:可以 但要改對歌詞拆字
# 問題2 : 為什麼只能找出三位歌手，第四位開始就不行 A: 試試sleep，慢一點
# 問題3 : 執行mojim時，能不能讓tab動作　A:沒辦法
# 問題4 : 為什麼Button不能直接print() A:因為()代表執行，可以丟到函式裡面

# 剩mojim背後執行chrome selenium headless V
# 圖形化 V
# 新增Label