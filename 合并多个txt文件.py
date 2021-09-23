#!/usr/bin/env python
# _*_coding: utf-8 _*_
# @Time : 2021/9/22 23:21
# @Author : CN-JackZhang
# @File: 合并多个txt文件.py
'''合并多个txt文件，并提取有效信息,并保存为dataframe文件，写入csv文件保存'''
import os
import re
import pandas as pd

def extract_txt():
    temp_data,time_data = [],[]  #创建两个列表装各自数据，用来合成dataframe
    files_list = os.listdir('../data/bmp')  #打开文件夹,获取文件夹下所有file的名称，同时也是记录日期信息
    '''1.读取'''
    for index in range(len(files_list)):                 # 遍历文件名
        if files_list[index].endswith('.txt'):  # 对每个文件进行筛选，只需要.txt结尾的，
            with open('../data/bmp/'+files_list[index]) as f:    # 然后打开这个txt文件.注意:bmp后面要加/，不然就会直接和后面文件名连接起来!
                line = f.read()     # 读取其中内容，
                # 用正则表达式匹配需要的字符串。温度和日期  '(.*?)'
                temp_data.append(re.compile('temp:(.*?)  x').findall(line)[0])    # 温度数据
                time_data.append(re.compile('(.*?)-2.txt').findall(files_list[index])[0])       # 时间数据
                f.close()
    df_data = pd.DataFrame(data={'temp':temp_data,'time':time_data})  #合并成dataframe，以字典形式输入data
    '''2.写入'''
    with open('../data/temp_time_data.csv',mode='w+') as fp:  # 打开一个事先创建好的csv文件temp_time_data.csv，装所有的txt
        df_data.to_csv(fp)         #写入csv文件
        fp.close()

    return df_data


def test():    #测试一下
    test = extract_txt()
    print(test)
    return None

test()