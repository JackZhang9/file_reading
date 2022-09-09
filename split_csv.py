#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# @Author:CN-JackZhang
# @Time:2022/9/9 16:27
# @File:split_csv.py
"""
对每一条路线的三个不同相，分别提取出具体连接部位的数据，有中间接头处，不同本体处
1.返回文件夹列表
2.遍历路径列表
3.打开一条路径，一个csv文件，创建一个文件句柄f,进行后续操作
4.取出每一条数据
5.取出一个位置
6.把两个得到的temp和time的list合并成一个dataframe
7.把这个dataframe输出到csv，用当前的路线名称命名
"""
import pandas as pd
import os
from pypinyin import lazy_pinyin as lp

# 显示设置：pandas显示一行全部数据
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)
# 设置value的显示长度为500，默认为50
pd.set_option('max_colwidth',500)

# 1.返回文件夹列表，如：['东科线', '乌海线', '图科线', '科呼牵线', '科海线', '科赛线']
files_list=os.listdir('F:\电缆\温度传感器')
# print('需要保存的路线有==>',files_list)

# 2.遍历路径列表
for folder_name in files_list:
    for phase in ['A', 'B', 'C']:
        rou_name_pinyin_list = lp(folder_name)
        rou_name_pinyin = ''.join(rou_name_pinyin_list)
        f_path='F:\电缆\温度传感器\\'+folder_name+'\\'+rou_name_pinyin+phase+'Phase.csv'
        print(f_path) # 路径没问题

        # f_path='F:\电缆\温度传感器\东科线\kehaixianAPhase.csv'
        # 3.打开一条路径，一个csv文件，创建一个文件句柄f,进行后续操作
        with open(f_path,encoding = "UTF-8") as f:
            routes = []  # 一条线路上的位置，存放个csv文件中，所有出现的位置，用作后续筛选
            temp_da = []  # 每次打开一个csv文件，初始化一个空的temp list和time list存放对应数据
            time_da = []
            # 获取所有内容的一个list
            datas=f.readlines()
            print('csv文件长度==>',len(datas),datas[1:3])

            # print(datas[1:5],type(datas))  # 查看数据
            # ['13.47,2020-12-02 08:41:09.341000,40.846379&111.727884,220kv东科线（东科7号-东科8号）-10号中间接头\n',
            # '13.3,2020-12-06 10:4
            # 4.取出每一条数据
            for i,data in enumerate(datas):
                # 表头不要，去掉第0行
                if i == 0:
                    continue
                # 取出线路位置
                route=data.split(',')[3]
                # 线路没有添加就加入，得到线路list
                if route not in routes:
                    routes.append(route)
            # 一次遍历路线列表，遍历每一条线路,如线路位置：本体800b相
            # 5.取出一个位置
            for one_rou in routes:
                # 在数据list中遍历，匹配所有位置一样的数据
                for one_da in datas:
                    # 将数据分割，得到对应属性，如：temp,route,time
                    data_list=one_da.split(',')
                    temp,time,rou=data_list[0],data_list[1],data_list[3]
                    # 如果线路位置一致，就保存对应的temp和time
                    if rou == one_rou:
                        temp_da.append(temp)
                        time_da.append(time)
                # 6.把两个得到的temp和time的list合并成一个dataframe
                cur_data=pd.DataFrame({'temp_list':temp_da,'time_data':time_da})
                # print('正在保存====>',rou+phase)
                # 7.把这个dataframe输出到csv，用当前的路线名称命名
                save_path='F:\电缆\温度传感器\\'+folder_name+'\\'+rou_name_pinyin+phase+'Phase'+'\\'+one_rou.strip()+phase+'Phase.csv'
                cur_data.to_csv(save_path,index=None,encoding='utf-8')
                print(''.join([rou + phase + '相', '====>', '保存完毕!']))
                print('-' * 100)
            f.close()

            # print(routes)  # 查看每条线路，
            # ['220kv东科线（东科7号-东科8号）-10号中间接头\n', '220kv东科线（东科7号-东科8号）-1号中间接头\n',
            #  '220kv东科线（东科7号-东科8号）-2号中间接头\n', '220kv东科线（东科7号-东科8号）-3号中间接头\n',
            #  '220kv东科线（东科7号-东科8号）-4号中间接头\n', '220kv东科线（东科7号-东科8号）-5号中间接头\n',
            #  '220kv东科线（东科7号-东科8号）-6号中间接头\n', '220kv东科线（东科7号-东科8号）-8号中间接头\n',
            #  '220kv东科线（东科7号-东科8号）-9号中间接头\n', '220kv东科线（东科7号-东科8号）-本体-100\n',
            #  '220kv东科线（东科7号-东科8号）-本体-1000\n', '220kv东科线（东科7号-东科8号）-本体-1100\n',
            #  '220kv东科线（东科7号-东科8号）-本体-1200\n', '220kv东科线（东科7号-东科8号）-本体-1400\n',
            #  '220kv东科线（东科7号-东科8号）-本体-1600\n', '220kv东科线（东科7号-东科8号）-本体-1700\n',
            #  '220kv东科线（东科7号-东科8号）-本体-1900\n', '220kv东科线（东科7号-东科8号）-本体-200\n',
            #  '220kv东科线（东科7号-东科8号）-本体-2100\n', '220kv东科线（东科7号-东科8号）-本体-2150\n',
            #  '220kv东科线（东科7号-东科8号）-本体-2300\n', '220kv东科线（东科7号-东科8号）-本体-2400\n',
            #  '220kv东科线（东科7号-东科8号）-本体-2500\n', '220kv东科线（东科7号-东科8号）-本体-2600\n',
            #  '220kv东科线（东科7号-东科8号）-本体-2700\n', '220kv东科线（东科7号-东科8号）-本体-2750\n',
            #  '220kv东科线（东科7号-东科8号）-本体-300\n', '220kv东科线（东科7号-东科8号）-本体-3000\n',
            #  '220kv东科线（东科7号-东科8号）-本体-3100\n', '220kv东科线（东科7号-东科8号）-本体-3300\n',
            #  '220kv东科线（东科7号-东科8号）-本体-3400\n', '220kv东科线（东科7号-东科8号）-本体-3600\n',
            #  '220kv东科线（东科7号-东科8号）-本体-3700\n', '220kv东科线（东科7号-东科8号）-本体-3800\n',
            #  '220kv东科线（东科7号-东科8号）-本体-500\n', '220kv东科线（东科7号-东科8号）-本体-600\n',
            #  '220kv东科线（东科7号-东科8号）-本体-700\n', '220kv东科线（东科7号-东科8号）-本体-800\n',
            #  '220kV东科线（东科9号-科尔沁变GIS）-1号中间接头\n', '220kV东科线（东科9号-科尔沁变GIS）-2号中间接头\n',
            #  '220kV东科线（东科9号-科尔沁变GIS）-本体-100\n', '220kV东科线（东科9号-科尔沁变GIS）-本体-300\n',
            #  '220kV东科线（东科9号-科尔沁变GIS）-本体-400\n', '220kV东科线（东科9号-科尔沁变GIS）-本体-600\n',
            #  '220kV东科线（东科9号-科尔沁变GIS）-本体-700\n', '220kV东科线（东科9号-科尔沁变GIS）-本体-800\n']









