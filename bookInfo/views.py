from django.shortcuts import render
from rest_framework.views import APIView
from .models import Bookcomment, Bookinfo
from rest_framework.views import APIView
from rest_framework.response import Response
# from .serializer import BookInfoSerializer
# from rest_framework.viewsets import ModelViewSet
from django.http import JsonResponse
from bookInfo.time_json import ymn_year, time_heatmap, ymn_array
from bookInfo.pesg_json import pesg_word, pos_list, pos_name
from bookInfo.wordcloud_json import wc_json
import json
# from pandas import Series, DataFrame
# import time
# import numpy as np
# import pandas as pd
# import traceback
# import psycopg2

# import http
# Create your views here.
# from rest_framework import permissions
# from rest_framework.response import Response
# from rest_framework.decorators import api_view, permission_classes
# from django.views.decorators.csrf import csrf_exempt


# class ScoreView(APIView):
#     def get(self, request):
#         print('hello')
#         book = Bookinfo.objects.get(sid=1007305)
#         print(book.score)
#         return book.score
#         # serializer = BookInfoSerializer(book.score)
#         # return Response(serializer.data)

class ScoreView(APIView):
    def get(self, request):
        book = Bookinfo.objects.get(sid=1007305)
        # resList = []
        res_score_Dict = {
            'sid': book.sid,
            'name': book.name,
            # 'tag': str(book.tag).strip('/').split('/'),
            'score': book.score,
            'tfidf': book.tfidf,
            # 'five_star': str(book.star).strip('/').split('/')[0],
            # 'four_star': str(book.star).strip('/').split('/')[1],
            # 'three_star': str(book.star).strip('/').split('/')[2],
            # 'two_star': str(book.star).strip('/').split('/')[3],
            # 'one_star': str(book.star).strip('/').split('/')[4],
            # 'year_list': ymn_year(time_heatmap(int(book.sid))),
            # 'mon_list': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'],
            # 'ym_num_list': ymn_array(time_heatmap(int(book.sid))),  # too long
            # 'wordcloud_image': "data:image/jpg;base64,{0}".format((wc_json(book.sid, 100))),
            # 'pesg_list': pos_list(int(book.sid)),
            # 'pesg_name': pos_name(int(book.sid)),
        }
        return JsonResponse(res_score_Dict, safe=False)


# class ScoreView(ModelViewSet):
#     queryset = Bookinfo.objects.all()
#     serializer_class = BookInfoSerializer


class SearchView(APIView):
    def get(self, request):
        bookname = request.query_params.get('bookname')
        book = Bookinfo.objects.get(name=bookname)
        res_Dict = {
            'sid': book.sid,
            'name': book.name,
            'score': book.score,
            'tag': str(book.tag).strip('/').split('/'),
            'five_star': str(book.star).strip('/').split('/')[0],
            'four_star': str(book.star).strip('/').split('/')[1],
            'three_star': str(book.star).strip('/').split('/')[2],
            'two_star': str(book.star).strip('/').split('/')[3],
            'one_star': str(book.star).strip('/').split('/')[4],
            'year_list': ymn_year(time_heatmap(int(book.sid))),
            'mon_list': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'],
            'ym_num_list': ymn_array(time_heatmap(int(book.sid))),
            'pesg_name': book.pesg_name,
            'pesg_list': book.pesg_list,
            'tfidf': book.tfidf,
            'word_cloud': book.word_cloud,
        }
        return JsonResponse(res_Dict, safe=False)


class StarView(APIView):
    def get(self, request):
        book = Bookinfo.objects.get(sid=1007305)
        # resList = []
        res_star_Dict = {
            'sid': book.sid,
            'name': book.name,
            'five_star': str(book.star).strip('/').split('/')[0],
            'four_star': str(book.star).strip('/').split('/')[1],
            'three_star': str(book.star).strip('/').split('/')[2],
            'two_star': str(book.star).strip('/').split('/')[3],
            'one_star': str(book.star).strip('/').split('/')[4],
            'year_list': ymn_year(time_heatmap(int(book.sid))),
            'mon_list': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'],
            'ym_num_list': ymn_array(time_heatmap(int(book.sid))),  # too long

        }
        return JsonResponse(res_star_Dict, safe=False)


class TimeView(APIView):
    def get(self, request):
        book = Bookinfo.objects.get(sid=1007305)
        # resList = []
        res_time_Dict = {
            'sid': book.sid,
            'name': book.name,
            'year_list': ymn_year(time_heatmap(int(book.sid))),
            'mon_list': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'],
            'ym_num_list': ymn_array(time_heatmap(int(book.sid))),  # too long
        }
        return JsonResponse(res_time_Dict, safe=False)


class PesgView(APIView):
    def get(self, request):
        book = Bookinfo.objects.get(sid=1007305)
        # resList = []
        tf_pos_dict = pesg_word(int(book.sid))
        res_pesg_Dict = {
            'sid': book.sid,
            'name': book.name,
            'pesg_list': pos_list(tf_pos_dict),
            'pesg_name': pos_name(tf_pos_dict),
        }
        return JsonResponse(res_pesg_Dict, safe=False)


class WrodcloudView(APIView):
    def get(self, request):
        book = Bookinfo.objects.get(sid=1007305)
        # resList = []
        res_score_Dict = {
            'sid': book.sid,
            'name': book.name,
            'wordcloud_image': "data:image/jpg;base64,{0}".format((wc_json(book.sid, 100)))
        }
        return JsonResponse(res_score_Dict, safe=False)


# class PgHandler(object):
#     def __init__(self, db="postgres", user="postgres", password=None, host="127.0.0.1", port="5432"):
#         '''
#         Args:
#             db: Database
#             user: Username
#             password: Password
#             host: Server
#             port: Port
#         '''
#         self.db = db
#         self.user = user
#         self.password = password
#         self.host = host
#         self.port = port
#         self.config = f'dbname = {self.db} \
#                         user = {self.user} \
#                         password = {self.password} \
#                         host = {self.host} \
#                         port = {self.port}'

#     def query(self, sql):
#         '''
#         Args:
#             sql: sql you want to query
#         '''
#         try:
#             conn = psycopg2.connect(self.config)
#             cur = conn.cursor()
#             cur.execute(sql)
#             res = cur.fetchall()
#             cur.close()
#             conn.close()
#             if not res:
#                 res = []
#             return res
#         except psycopg2.Error as e:
#             print(str(traceback.format_exc()))
#             return

#     def execute(self, sql):
#         '''
#         Args:
#             sql: sql you want to execute
#         '''
#         try:
#             conn = psycopg2.connect(self.config)
#             cur = conn.cursor()
#             cur.execute(sql)
#             res = None
#             if "returning" in sql:
#                 res = cur.fetchone()
#             conn.commit()
#             cur.close()
#             conn.close()
#             return res
#         except psycopg2.Error as e:
#             print(str(traceback.format_exc()))


# def Sql_select_time(sid):
#     sql_insert = 'SELECT TIME FROM BOOK_COMMENT WHERE (SID = {0});'.format(sid)
#     return sql_insert


# def time_data(sid):
#     pg = PgHandler("testdb", "postgres", "6666")
#     sql = Sql_select_time(sid)
#     datas = pg.query(sql)
#     return datas


# def parse_ymd(list_):
#     tt_list = []
#     for t in list_:
#         t = eval(str(t).strip('(').strip(')').strip(','))
#         year_s, mon_s, day_s = t.split('-')
#         tt = str(year_s+'-'+mon_s)
#         # print(tt)
#         tt_list.append(tt)
#     return tt_list


# def time_ddict(tt_list):
#     year_dict = {}  # 定义一个存放年份的字典套空字典
#     inner_dict = {}
#     for i in range(1, 13):
#         inner_dict[str(i).zfill(2)] = int(0)   # 定义一个内层字典
#     tf_dict = {}  # 定义一个存放月份频数的字典

#     for t in tt_list:  # 遍历清洗过的YYYY-MM列表
#         year_s, mon_s = t.split('-')  # 将年月分开
#         year_dict[year_s] = inner_dict  # 将年份字典存入key（年份）、value（空字典）
#         if t in tf_dict:  # 制作一个年月频数字典key（YYYY-MM）、value（频数）
#             tf_dict[t] += 1
#         else:
#             tf_dict[t] = 1
#     year_dict = sorted(year_dict.items(),
#                        key=lambda item: item[0], reverse=False)
#     year_dict = dict(year_dict)

#     for tf_year_mon, tf in tf_dict.items():  # 遍历年月频数字典的key（YYYY-MM）、value（频数）
#         add_dict = {}
#         tf_year, tf_mon = tf_year_mon.split('-')    # 将年月分开
#         add_dict[str(tf_mon).zfill(2)] = int(tf)    # 制作月份对应词频键值对
#         a = year_dict.get(tf_year)                  # 创建一个对象保存年份字典中年份所对应的value
#         a = dict(a)                                 # 转化为字典格式
#         a.update(add_dict)                          # 将月份键值对添加到a上
#         # 最后将a作为年份字典的value，以此循环更新所有月份频率
#         year_dict[tf_year] = a
#     return year_dict


# def time_heatmap(sid):
#     datas = time_data(sid)
#     tt_list = parse_ymd(datas)
#     time_dict = time_ddict(tt_list)
#     return time_dict


# def ymn_year(time_dict):
#     year_list = []
#     for year, month_dict in time_dict.items():
#         year_list.append(year)
#     return year_list


# def ymn_array(time_dict):
#     year_list = []
#     ym_num = []
#     all_ym_num = []
#     for year, month_dict in time_dict.items():
#         year_list.append(year)
#         for month, num in month_dict.items():
#             ym_num = [int(year)-int(min(year_list)), int(month)-1, int(num)]
#             all_ym_num.append(ym_num)
#     print(all_ym_num)
#     print(year_list)
#     return all_ym_num
