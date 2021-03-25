import pandas as pd
import jieba
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
import os
import random

def poemcut(p):
    return " ".join(jieba.cut(p))

def  __init__(inp):

    if os.path.exists("2020華語歌手排行前五位.csv"):

        data={}

        train_df = pd.read_csv("2020華語歌手排行前五位.csv", encoding="utf-8")
        u = train_df["word_name"].unique() # 列出所有陣列的元素(不重複)

        name2cat = {name:i for i, name in enumerate(u)}
        # cat2name = {i:name for i, name in enumerate(u)}
        y_traub = train_df["word_name"].replace(name2cat)

        x_train = train_df["lyrics"].apply(poemcut)

        vec = CountVectorizer()
        x_train_count = vec.fit_transform(x_train)

        clf = MultinomialNB(alpha=0.01)
        clf.fit(x_train_count, y_traub)

        pre = clf.predict(x_train_count)
        accuracy_score(pre, y_traub)

        mat = confusion_matrix(y_traub, pre)

        pd.DataFrame(mat,
                        index=[name + "(原本)" for name in u],
                        columns=[name + "(預測)" for name in u])

        p = inp
        test = vec.transform([poemcut(p)])
        prob = clf.predict_proba(test)[0]
        for i in range(len(u)):
            data.setdefault(u[i],round(prob[i], 3))
            # print("\n"+u[i],"的機率:{}".format(round(prob[i], 3)))
        # print(data)
        # print(data.keys())

        return data
