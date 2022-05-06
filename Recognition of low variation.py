# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 20:04:29 2022

@author: lifufu
"""

#结果1过滤 以30轮廓分检验大于比例尺长度的ratio变异小于0.1

import pandas as pd
from numpy import mean, std
import os
import shutil

#提取cv小的图
#path= r"F:\colorseed\2\csv\seeddata.csv" 
#path_pic= r"F:\colorseed\2\seednormal"      
def acc(path,path_pic):
    data=pd.read_csv(path) 
    list1=data["name"]
    list2=[]
    [list2.append(i) for i in list1 if not i in list2]# 获取name
    acc=[]
    for i in list2:
        a=list1[list1.values == i].index  # 根据值获取索引
        df =data[a[0]:a[-1]+1]["ratio"] 
        df=df.to_numpy() # 获得ratio
        cv= std(df)/mean(df)
        if cv<=0.1:#阈值标准
            acc.append(i)
    #新数据保存
    data['True'] = ''
    for j in acc:
        a=list1[list1.values == j].index #正确值的索引
        data.at[a,'True']=1
    data.to_csv(path)
    #图片移动
    path1= os.path.join(path_pic,"acc")#需自动创建新acc
    if not os.path.exists(path1):
        os.makedirs(path1)#不存在路径则创建
    for i in acc:
        shutil.move(os.path.join(path_pic,i+".jpg") ,os.path.join(path1,i+".jpg"))
    return data,acc






#运行20文件夹 seedabnormal
for i in range(2,21,1):
    print(i)
    
    
    path= os.path.join("F:\colorseed",str(i),"csv\seedabn.csv")
    path_pic= os.path.join("F:\colorseed",str(i),"seedabnormal")
    
    def acc(path,path_pic):
        data=pd.read_csv(path) 
        list1=data["name"]
        list2=[]
        [list2.append(i) for i in list1 if not i in list2]# 获取name
        acc=[]
        for i in list2:
            a=list1[list1.values == i].index  # 根据值获取索引
            df =data[a[0]:a[-1]+1]["ratio"] 
            df=df.to_numpy() # 获得ratio
            cv= std(df)/mean(df)
            if cv<=0.1:#阈值标准
                acc.append(i)
        #新数据保存
        data['True'] = ''
        for j in acc:
            a=list1[list1.values == j].index #正确值的索引
            data.at[a,'True']=1
        data.to_csv(path)
        #图片移动
        path1= os.path.join(path_pic,"acc")#需自动创建新acc
        if not os.path.exists(path1):
            os.makedirs(path1)#不存在路径则创建
        for i in acc:
            shutil.move(os.path.join(path_pic,i+".jpg") ,os.path.join(path1,i+".jpg"))
        return data,acc

    
    data,acc=acc(path,path_pic)



#自动生成文件夹
path_pic="F:\colorseed\结果1"
for i in range(2,20,1):
    path1= os.path.join(path_pic,str(i))#需自动创建新acc
    if not os.path.exists(path1):
        os.makedirs(path1)#不存在路径则创建
#自动移动文件夹
for i in range(2,21,1):
    print(i)
    path= os.path.join(r"F:/colorseed",str(i),"seednormal/acc")
    path1= os.path.join(r"F:/colorseed/结果1",str(i),"seednormal/acc")
    shutil.move(path,path1) 









