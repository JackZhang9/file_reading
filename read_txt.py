#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# @Author:CN-JackZhang
# @Time:2022/9/7 16:27
# @File:read_txt.py
"""
读取数据，查看数据，提取数据，输出数据
1.打开文件夹，获取文件夹下所有文件夹名的列表
2.循环获取文件路径
3.创建一个文件句柄，用于后续操作
4.保存温度数据
5.保存时间数据
6.保存路线数据
7.保存位置数据
8.将4个list合并成一个dataframe
9.将汉字转化为拼音,用于在保存时组成csv文件的名字
10.将数据输出到datas.csv文件
"""
import pandas as pd
import re
import os
from pypinyin import lazy_pinyin as lp

# 显示设置：pandas显示一行全部数据
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)
# 设置value的显示长度为500，默认为50
pd.set_option('max_colwidth',500)

# 1.打开文件夹，获取文件夹下所有文件夹名的列表
files_list=os.listdir('F:\电缆\温度传感器')
print('需要保存的路线有==>',files_list)  # 查看文件夹列表，如：['东科线', '乌海线', '图科线', '科呼牵线', '科海线', '科赛线']

# 2.循环获取文件路径
for rou in files_list:  # 遍历路径列表
    print('读取==>',rou)  # 查看rou，如：东科线 <class 'str'>
    for x in ['a','b','c']:  # 遍历创建的a,b,c相列表
        # debug，之前已经保存了东科线，乌海线,图科线，科呼牵线，科海线，科赛线的a相
        if rou=='东科线' or rou=='图科线' or rou=='乌海线'or rou=='科呼牵线' or rou=='科海线' or (rou=='科赛线' and x=='a'):
            continue
        # 生成一条path
        f_path='F:\电缆\温度传感器\\'+rou+'\\'+rou+'温度传感器'+x+'相.txt'  # 注意：python中反斜杠是转义字符，要用\\表示\
        print('当前路线==>',f_path)

        # 正确的文件路径,如：f_path=r"F:\电缆\温度传感器\东科线\东科线温度传感器c相.txt"

        id_data=[]  # 保存数据id
        cnt_temp=0
        # 3.创建一个文件句柄，用于后续操作
        with open(f_path,encoding = "UTF-8") as f:
            temp_data, time_data, pos_data, rou_data = [], [], [], []  # 创建4个列表装各自数据，温度，时间，位置，路线，共4个list，用来合成dataframe
            data=f.readlines()   # 返回一个每一行数据的list

            # print('data len==>',len(data))
            for i,line in enumerate(data):
                if i == 0:  # 跳过第一行
                    id_data.append(line.split())  # 将第一行保存到id列表
                    continue
                line=line.split('\t')  # 0,1,2,3分别是：年月日时分秒，路线，位置，温度
                # debug,有空字符串就不用那一行,直接跳过
                if line[0]=='' or line[1]=='' or line[2]=='' or line[3]=='\n':
                    continue
                # debug，查看每一条数据具体内容,186052
                # if i>186050 and i<186055:
                #     print(i,line)
                # print(len(line[3]))  # 查看温度数据长度

                # 4.保存温度数据，温度数据经分析有3类，如7.2, 18.8, 19.47，对于不同长度字符串，不同保存模式,保存为浮点型数值
                if len(line[3])==8:   # 6,4 ||7,5||8,6，如：19.47
                    temp_data.append(float(line[3][1:6]))  # 用[1:6]取出温度字符串如：7.2
                elif len(line[3])==7:  # 如：18.8
                    temp_data.append(float(line[3][1:5]))
                elif len(line[3])==6:  # 如：7.2
                    temp_data.append(float(line[3][1:4]))
                elif len(line[3])==9:     # 如：-10.72
                    temp_data.append(float(line[3][1:7]))  # 添加温度数据
                elif len(line[3])==5:    # 如：50
                    temp_data.append(float(line[3][1:3]))
                # debug时用，如温度数据比其他数据少几条，温度问题都能从这debug到
                # cnt_temp += 1  # 温度计数+1
                # if cnt_temp==len(temp_data):  # 查看温度数据总数和循环次数总数是否相等
                #     # print('cnt_temp==>',cnt_temp)
                #     # print(i,len(temp_data))
                #     # pass
                # else:  # 如果不相等，看是因为哪一个温度数据，看原因
                #     print(i,'==>',line[3])

                # 5.保存时间数据,如：2020-12-02 08:41:09.341
                time_str=re.findall('"(.*?)"',line[0])[0]  # 正则表达式提取出时间数据，原始数据是字符串''中的一个字符串,返回一个list，用[0]取出
                if len(time_str)==22 or len(time_str)==21:   # 经测试长度为22，21或18，当长度为21或22时有毫秒3位
                    time_data_p=pd.to_datetime(time_str,format='%d/%m/%Y %H:%M:%S.%f')
                elif len(time_str)==18:  # 当长度为18时，无毫秒位3位，需要加上毫秒位，在末尾加上+'.0'
                    time_str=time_str+'.0'
                    time_data_p = pd.to_datetime(time_str, format='%d/%m/%Y %H:%M:%S.%f')
                time_data_p=str(time_data_p)
                # print(time_data_p,type(time_data_p))  # 查看时间戳和时间戳的数据类型
                time_data.append(time_data_p)   # 添加时间数据

                # 6.保存路线数据，如：220kv东科线（东科7号-东科8号）-10号中间接头
                rou_str=re.findall('"(.*?)"',line[1])  # 正则表达式提取出路线数据，原始数据是字符串''中的一个字符串,返回一个list，用[0]取出
                # debug:查看路线字符串
                if rou_str!=None:
                    # print(i,'==>','str is not None')
                    rou_data.append(rou_str[0])  # 添加路线数据
                else:
                    print('str is None!!!')
                # 7.保存位置数据，如：40.846379&111.727884
                pos_str=re.findall('"(.*?)"',line[2])[0]  # 正则表达式提取出路线数据，原始数据是字符串''中的一个字符串,返回一个list，用[0]取出
                pos_data.append(pos_str)  # 添加位置数据

            f.close()   # 关闭句柄

        # debug,查看一下数据，需要时查看，List长度不一致时都能从这debug到,
        # print('temp==>',len(temp_data),type(temp_data))  # 685856 <class 'list'>
        # print('time==>',len(time_data),type(time_data))  # 685856 <class 'list'>
        # print('rou==>',len(rou_data),type(rou_data))    # 685856 <class 'list'>
        # print('pos==>',len(pos_data),type(pos_data))    # 685856 <class 'list'>
        '''数据以空格隔开'''

        # 8.将4个list合并成一个dataframe
        # 把多个list合并为dataframe并输出到csv文件， temp_data, time_data, pos_data, rou_data
        datas=pd.DataFrame({'temp_list':temp_data,'time_data':time_data,'pos_list':pos_data,'rou_list':rou_data})
        # print(datas.head())  # 查看一下前5行内容
        #  temp_list               time_data              pos_list         rou_list
        # 0      13.47 2020-12-02 08:41:09.341  40.846379&111.727884  220kv东科线（东科7号-东科8号）-10号中间接头
        # 1      13.30 2020-12-06 10:43:34.688  40.846379&111.727884  220kv东科线（东科7号-东科8号）-10号中间接头
        # 2      13.21 2020-12-06 11:46:55.638  40.846379&111.727884  220kv东科线（东科7号-东科8号）-10号中间接头
        # 3      13.12 2020-12-06 12:02:42.562  40.846379&111.727884  220kv东科线（东科7号-东科8号）-10号中间接头
        # 4      13.21 2020-12-06 12:04:48.041  40.846379&111.727884  220kv东科线（东科7号-东科8号）-10号中间接头

        # 9.将汉字转化为拼音,用于在保存时组成csv文件的名字
        rou_name_pinyin_list=lp(rou)
        rou_name_pinyin=''.join(rou_name_pinyin_list)
        print('正在保存为==>',rou_name_pinyin)  # 查看汉字转化为的拼音

        # 10.将数据输出到datas.csv文件
        # to_csv是DataFrame类的方法，如datas.to_csv默认datas是DataFrame的一个实例
        save_path='F:\电缆\温度传感器\\'+rou+'\\'+rou_name_pinyin+x.upper()+'Phase.csv'  #小写字符变大写字符
        datas.to_csv(save_path,index=None,encoding='utf-8-sig')  # index=None输出文件不加行号,'utf-8-sig'解决中文乱码

        print(rou+x+'相','==>','保存完毕!')
        print('-'*50)
        '''至此，数据已保存为csv文件'''






