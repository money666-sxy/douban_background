import math
import operator
import multiprocessing
from itertools import chain
import jieba.posseg as pseg
import jieba
import psycopg2
import traceback
import wordcloud
import time
import base64
jieba.posseg.POSTokenizer(tokenizer=jieba.Tokenizer())


class PgHandler(object):
    def __init__(self, db="postgres", user="postgres", password=None, host="127.0.0.1", port="5432"):
        '''
        Args:
            db: Database
            user: Username
            password: Password
            host: Server
            port: Port
        '''
        self.db = db
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.config = f'dbname = {self.db} \
                        user = {self.user} \
                        password = {self.password} \
                        host = {self.host} \
                        port = {self.port}'

    def query(self, sql):
        '''
        Args:
            sql: sql you want to query
        '''
        try:
            conn = psycopg2.connect(self.config)
            cur = conn.cursor()
            cur.execute(sql)
            res = cur.fetchall()
            cur.close()
            conn.close()
            if not res:
                res = []
            return res
        except psycopg2.Error as e:
            print(str(traceback.format_exc()))
            return

    def execute(self, sql):
        '''
        Args:
            sql: sql you want to execute
        '''
        try:
            conn = psycopg2.connect(self.config)
            cur = conn.cursor()
            cur.execute(sql)
            res = None
            if "returning" in sql:
                res = cur.fetchone()
            conn.commit()
            cur.close()
            conn.close()
            return res
        except psycopg2.Error as e:
            print(str(traceback.format_exc()))


def corpus(sid):
    pg = PgHandler("postgres", "postgres", "6666")
    datas = pg.query(
        'SELECT comment FROM public."bookInfo_bookcomment" WHERE (SID = {0});'.format(sid))
    corpus = []
    for data in datas:  # 按行取出语料库——文档
        one_document = []
        for word in jieba.cut(str(data).strip('(').strip(')').strip(',')):
            if len(word) >= 2 and len(word) <= 5:
                # one_document = tuple([word])
                one_document.append(word)
        corpus.append(one_document)  # 合成语料库

    # print('语料库：', corpus)
    # print('总文档数：', len(corpus))  # 总文档数用nd表示
    return corpus


def tf(corpus_list: list):
    '''
    输入语料库
    字典计数
    返回词频字典
    '''
    tf = {}
    for document in corpus_list:
        for word in document:
            if word in tf:
                tf[word] += 1
            else:
                tf[word] = 1
    return tf


def nd(corpus_list: list):
    '''
    nd 代表总文档数
    '''
    return len(corpus_list)


def df(word: str, corpus_list: list):
    '''
       df（d，t） 代表包含特征值t的文档数
    '''
    count = 0
    for document in corpus_list:
        count += document.count(word)
    return count


def pos(list, num):
    '''
    过滤词性、限制输出列表长度
    '''
    pos_dict = {}
    fianal_list = []
    for i in list:
        pos_dict.update(dict(pseg.lcut(i)))
    # print(pos_dict)
    for word, flag in pos_dict.items():
        if flag != 'm' and flag != 'q' and flag != 'p' and flag != 'r' and flag != 'c' and flag != 'u' and flag != 'w' and flag != 'xc' and flag != 'd' and flag != 'eng':
            if len(word) > 1:
                fianal_list.append(word)
    return fianal_list[:num]


def tfidf(sid, num: int):
    corpus_list = corpus(sid)
    # print('语料库：', corpus_list)
    tf_dict = tf(corpus_list)
    # print('词频字典：', tf_dict)
    nd_valuse = nd(corpus_list)
    # print('nd的值：', nd_valuse)
    tfidf_dict = {}
    for word in tf_dict.keys():
        df_valuse = df(word, corpus_list)
        idf = math.log((nd_valuse+1)/(df_valuse+1)) + 1
        tf_idf = tf_dict[word] * idf
        # print(word, 'tfidf:', tf_idf, 'tf:',
        #       tf_dict[word], 'nd:', df_valuse, 'idf:', idf)
        tfidf_dict[word] = tf_idf
    sorted_dict = dict(
        sorted(tfidf_dict.items(), key=lambda item: item[1], reverse=True))
    sorted_list = list(sorted_dict.keys())
    # print(wash_list[:50])
    # print(pos(sorted_list, num))
    weight_list = pos(sorted_list, num)
    # print('手写算法筛选出的特征词:', weight_list)
    return weight_list


def word_cloud(data: list):
    # stopWords_dic = open(
    #     '/Users/money666/Desktop/stopwords/stopwords.txt', 'r', encoding='utf-8')     # 从文件中读入停用词
    # stopWords_content = stopWords_dic.read()
    # stopWords_list = stopWords_content.splitlines()     # 转为list备用
    # stopWords_dic.close()

    w = wordcloud.WordCloud(background_color="black",
                            font_path='/Users/money666/Desktop/字体/粗黑.TTF',
                            width=1400, height=900, scale=1)  # stopwords=stopWords_list
    txt = ' '.join(data)
    w.generate(txt)
    w.to_file("/Users/money666/Desktop/django_douban/wordcloud_database.png")


def wc_json(sid, num):
    tfidf_list = tfidf(sid, num)
    word_cloud(tfidf_list)
    bb = base64.b64encode(open(
        "/Users/money666/Desktop/django_douban/wordcloud_database.png", 'rb').read())
    return eval(str(bb).strip('b'))


if __name__ == "__main__":
    start = time.time()
    # sid = 34617196  # 看见 20427187
    sid = '1007305'
    data = wc_json(sid, 100)
    print(data)
    print(time.time()-start)
