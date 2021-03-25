import time
from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
# from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen

data = dict() # 存歌名、歌名網址
data_singer = {
    "singer":[],
    "songtitle":[],
    "word_name":[],
    "lyrics":[]
} # singer存歌手、songtitle歌名、word_name存作詞人、lyrics歌詞

def keyword(inp):

    # htmlurl = driver.current_url # 可以抓取當前網址
    # print(htmlurl)
    # -----------------------------------
    # driver = Chrome("./chromedriver")
    # driver.create_options()
    # driver.get("https://mojim.com/")
    # ----------------------------------- 背景執行
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path="./chromedriver",
                              chrome_options=options)
    driver.get("https://mojim.com/")
    # -----------------------------------
    driver.maximize_window()
    driver.find_element_by_xpath('//input[@value="1"]').send_keys(Keys.SPACE) # radio的選擇
    e1 = driver.find_element_by_name("keyword") # 找name
    e1.clear()
    e1.send_keys(inp)
    e1.send_keys(Keys.ENTER)
    eu = driver.find_elements_by_class_name("mxsh_ulz") # 找到class的name
    loop2(inp,eu)

def loop2(inp,eu):
    # 步驟1---------------------------------------------------- 缺隱藏執行

    # 首頁的class_name="mxsh_ulz"是ul
    for i in eu:
        # 把ul裡面的li抓出來
        el = i.find_elements_by_tag_name("li")
        # print(link.text)
        for l in el:
            # 把li裡面的a抓出來
            link = l.find_element_by_tag_name("a")
            # print(link.text) # 先不列印出來
            # print(link.get_attribute("href")) # 先不列印出來
            if link.text == inp:
                # link.send_keys(Keys.ENTER) # 只對"指定歌手名稱"點擊下去
                url = link.get_attribute("href") # 取href的內容
                endless_loop(inp,url)
                # print("loop2")

def endless_loop(inp,url):
    # 步驟2----------------------------------------------------可以寫成函式
    response = urlopen(url)
    html = bs(response)

    ins = html.find("div", id="frame").find("div", id="Tb3").find("div",id="inS").find("dl", class_="ha0")
    hb2 = ins.find_all("dd", class_="hb2")
    # hb2 = ins.find_all("dd", {"class":"hb2", "class":"hb3"}) #不能這樣寫
    hb3 = ins.find_all("dd", class_="hb3")

    def datahb(hb):

        for hc in hb:
            # print(hc.get_text())
            # print(hc.text)

            a3 = hc.find_all("a")
            # print(a3[0]["href"])

            for i in range(len(a3)):
                if a3[i]["href"][1:4] == "twy":  # 只留歌詞跟歌詞網址
                    data.setdefault(a3[i].text, "https://mojim.com"+a3[i]["href"])
                else:
                    continue
                    # print("預留專輯與專輯網址")
                    # print(a3[i].text)
                    # print(a3[i]["href"])

            # data.setdefault(a3.text,a3["href"])
            # data[a3.text] = a3["href"]
    datahb(hb2)
    datahb(hb3)

    # ---------------------------------------------------------
    # 步驟3---------------------------------------------------- 抓歌詞

    key_name = list(data.keys()) # dict.keys()會顯示dict(list)，如果要抓list出來，要用list包覆
    # print(data[key_name[0]])
    for i in range(len(key_name)):
        url = data[key_name[i]] # 要寫迴圈
        response = urlopen(url) # 可以寫成def
        html = bs(response)
        ins = html.find("div", id="frame").find("div", id="Tb3").find("table").find_all("tr")[1].find("td").find("div",id="ss_y_tb3_1").find("table").find("div",id="fsZ").find("dl",id="fsZx1").find("dd",id="fsZx3")

        # ----------------------------------- 找出作詞者
        word_find_star = ins.text.find("作詞")
        song_find_end = ins.text.find("作曲")
        # print(key_name[i])
        # print("word_find_star:",word_find_star)
        # print("song_find_end:", song_find_end)
        # print(ins.text[word_find_star+3:song_find_end])
        # print("data_singer[singer]", len(data_singer["singer"]))
        # print("data_singer[songtitle]", len(data_singer["songtitle"]))
        # print("data_singer[word_name]", len(data_singer["word_name"]))
        # print("data_singer[lyrics]", len(data_singer["lyrics"]))
        # print("*"*100)
        if word_find_star != -1 :
            if song_find_end != -1:
                if word_find_star < song_find_end :
                    if ins.text[word_find_star + 3:song_find_end] == inp:
                        data_singer["word_name"].append(ins.text[word_find_star + 3:song_find_end])
                        # -----------------------------------　找出歌詞
                        lyrics_star = ins.text.find("編曲")
                        lyrics_end = ins.text.find("[")

                        if lyrics_star != -1:
                            data_singer["lyrics"].append(ins.text[lyrics_star + 6:-1])
                        elif lyrics_star != -1 and lyrics_end != -1:
                            data_singer["lyrics"].append(ins.text[song_find_end + 6:lyrics_end])
                        else:
                            data_singer["lyrics"].append(ins.text)
                        # -----------------------------------
                        data_singer["singer"].append(inp)  # 存歌手名
                        data_singer["songtitle"].append(key_name[i])  # 歌曲名
                        # print(data_singer)
                        # ---------------------------------------------------------
                else:
                    continue
            else:
                continue
        else:
            continue
        # if word_find_star != -1 and song_find_end != -1:
        #     data_singer["word_name"].append(ins.text[word_find_star+3:song_find_end])
        # if word_find_star != -1:
        #     data_singer["word_name"].append(ins.text[word_find_star+3:song_find_end])
        # else:
        #     data_singer["word_name"].append(inp)
        # print(word_name)
        # -----------------------------------

def __init__(inp):

    keyword(inp)
    return data_singer



# inp = input("請輸入歌手:")
#
# driver = Chrome("./chromedriver")
# driver.create_options()
# driver.get("https://mojim.com/")
# driver.maximize_window()
# driver.find_element_by_xpath('//input[@value="1"]').send_keys(Keys.SPACE) # radio的選擇
# # https://huilansame.github.io/huilansame.github.io/archivers/radio-button-checkbox
# keyword(inp)
