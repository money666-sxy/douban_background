from pandas import Series, DataFrame
import time
import numpy as np
import pandas as pd
import traceback
import psycopg2


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


def Sql_select_time(sid):
    sql_insert = 'SELECT TIME FROM public."bookInfo_bookcomment" WHERE (SID = {0});'.format(
        sid)
    return sql_insert


def time_data(sid):
    pg = PgHandler("postgres", "postgres", "6666")
    sql = Sql_select_time(sid)
    datas = pg.query(sql)
    return datas


def parse_ymd(list_):
    tt_list = []
    for t in list_:
        t = eval(str(t).strip('(').strip(')').strip(','))
        year_s, mon_s, day_s = t.split('-')
        tt = str(year_s+'-'+mon_s)
        # print(tt)
        tt_list.append(tt)
    return tt_list


def time_ddict(tt_list):
    year_dict = {}  # 定义一个存放年份的字典套空字典
    inner_dict = {}
    for i in range(1, 13):
        inner_dict[str(i).zfill(2)] = int(0)   # 定义一个内层字典
    tf_dict = {}  # 定义一个存放月份频数的字典

    for t in tt_list:  # 遍历清洗过的YYYY-MM列表
        year_s, mon_s = t.split('-')  # 将年月分开
        year_dict[year_s] = inner_dict  # 将年份字典存入key（年份）、value（空字典）
        if t in tf_dict:  # 制作一个年月频数字典key（YYYY-MM）、value（频数）
            tf_dict[t] += 1
        else:
            tf_dict[t] = 1
    year_dict = sorted(year_dict.items(),
                       key=lambda item: item[0], reverse=False)
    year_dict = dict(year_dict)

    for tf_year_mon, tf in tf_dict.items():  # 遍历年月频数字典的key（YYYY-MM）、value（频数）
        add_dict = {}
        tf_year, tf_mon = tf_year_mon.split('-')    # 将年月分开
        add_dict[str(tf_mon).zfill(2)] = int(tf)    # 制作月份对应词频键值对
        a = year_dict.get(tf_year)                  # 创建一个对象保存年份字典中年份所对应的value
        a = dict(a)                                 # 转化为字典格式
        a.update(add_dict)                          # 将月份键值对添加到a上
        # 最后将a作为年份字典的value，以此循环更新所有月份频率
        year_dict[tf_year] = a
    return year_dict


def time_heatmap(sid):
    datas = time_data(sid)
    tt_list = parse_ymd(datas)
    time_dict = time_ddict(tt_list)
    return time_dict


def ymn_year(time_dict):
    year_list = []
    for year, month_dict in time_dict.items():
        year_list.append(year)
    return year_list


def ymn_array(time_dict):
    year_list = []
    ym_num = []
    all_ym_num = []
    for year, month_dict in time_dict.items():
        year_list.append(year)
        for month, num in month_dict.items():
            ym_num = [int(year)-int(min(year_list)), int(month)-1, int(num)]
            all_ym_num.append(ym_num)
    print(all_ym_num)
    print(year_list)
    return all_ym_num
