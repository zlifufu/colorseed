# -*- coding: utf-8 -*-
"""
Created on Fri Dec 31 19:52:52 2021

@author: lifufu
"""

import cv2 as cv
from PIL import ImageFont, ImageDraw,Image
import numpy as np
import pandas as pd
import os
import time


#函数
#获取地址内的文件列表
def namelist(path):
    list1 = [i for i in os.listdir(path)]
    return list1


#边缘检测 膨胀 轮廓识别
def canny_demo(image,t=200,e=2):#输入图片和阈值
    #image = cv.GaussianBlur(image, (9, 17), 0)#高斯模糊参数？直接没轮廓了
    canny_output = cv.Canny(image, t, t * 2)
    k = np.ones((e, e), dtype=np.uint8)
    binary = cv.morphologyEx(canny_output, cv.MORPH_DILATE, k)
    contours, hierarchy = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    return contours
#contours=canny_demo(image)

#比例尺设为2,计算contours所有轮廓参数
def conparam(contours):
    area1=[]
    arclen1=[]
    lenth1=[]
    width1=[]
    Ratio1=[]
    sumlw1=[]      
    for i in range(len(contours)):
        #像素值的周长面积
        area = cv.contourArea(contours[i])
        arclen = cv.arcLength(contours[i], True)#轮廓闭合
        #外接矩形
        rect = cv.minAreaRect(contours[i]) # 得到最小外接矩形的（中心(x,y), (宽,高), 旋转角度）
        box = cv.boxPoints(rect) # 获取最小外接矩形的4个顶点坐标(ps: cv2.boxPoints(rect) for OpenCV 3.x)
        box = np.int0(box)
        erc=rect[0]#中心点坐标
        erw=rect[1][0]#宽度
        erh=rect[1][1]#高度
        erang=rect[2]#水平旋转角度
        if erw>erh:
            lenth=erw
            width=erh
        else:
            lenth=erh
            width=erw 
        
        if width==0:
            Ratio=0.1
        else:
            Ratio=lenth/width
            
        sumlw=lenth+width
        area1.append(area)
        arclen1.append(arclen)
        width1.append(width)
        lenth1.append(lenth)
        Ratio1.append(Ratio)
        sumlw1.append(sumlw)
        
    #比例尺索引
    scale_index = Ratio1.index(max(Ratio1))
    tsjl=lenth1[scale_index]
    #比例尺实际距离计算
    sjjl=2
    kdbs=tsjl/2#比例尺参数 图上扩大倍数 
    #比例尺测试 为矩形则为比例尺
    area_scale =lenth1[scale_index]*width1[scale_index]/kdbs/kdbs
    ste1= [ i*0 for i in Ratio1 ]
    ste1[scale_index]=round(area_scale,2)
    #计算实际值
    area1= [ round(i/kdbs/kdbs,2) for i in area1 ]
    arclen1= [ round(i/kdbs,2) for i in arclen1]
    lenth1= [ round(i/kdbs,2) for i in lenth1]
    width1= [ round(i/kdbs,2) for i in width1]
    sumlw1= [ round(i/kdbs,2) for i in sumlw1]
    Ratio1= [ round(i,2) for i in Ratio1]
    seedimg = pd.DataFrame({'area':area1,'cir':arclen1,'lenth':lenth1,'width':width1,'sumlw':sumlw1,'ratio':Ratio1,'ste':ste1}) #area1,arclen1,erw1,erh1,Ratio
    return seedimg,lenth1,scale_index#所有参数 长度  比例尺轮廓参数索引
#seedimg,lenth,scale_index=conparam(contour)

#比例尺设为2 抽取种子参数和需标记的索引 长度大于2的轮廓抽取出来
def seedr(seedimg,lenth,scale_index):
    sjjl=2
    seed=seedimg[0:0]
    seedindex=[]
    for i in lenth:
        if i>sjjl:
            a=lenth.index(i)
            s=pd.DataFrame(seedimg.iloc[a])
            s = pd.DataFrame(s.values.T, index=s.columns, columns=s.index)#转置
            seed=seed.append(s)
            seedindex.append(a)
    seedis=[]
    seedis=seedindex+[scale_index] 
    return seed,seedis
#seed,seedis=seedr(seedimg,lenth,scale_index)

#绘制外接框和标注
def seedvis(contours,seedimg,seedis,imgs):
    ft = ImageFont.truetype("F:\seed\TimesNewRoman.TTF", 15)
    for i in seedis:
        #外接矩形
        rect = cv.minAreaRect(contours[i]) # 得到最小外接矩形的（中心(x,y), (宽,高), 旋转角度）
        box = cv.boxPoints(rect) # 获取最小外接矩形的4个顶点坐标(ps: cv2.boxPoints(rect) for OpenCV 3.x)
        box = np.int0(box)
        erc=rect[0]#中心点坐标
        #绘制文字信息
        img_pil = Image.fromarray(imgs)
        draw = ImageDraw.Draw(img_pil)
        draw.text(erc,  str(seedimg[i:i+1]), font=ft, fill = (0, 0, 0))
        imgs = np.array(img_pil)
        #绘制外接矩形
        cv.drawContours(imgs, [box], 0, (255, 0, 0), 1)
    #绘制轮廓
    cv.drawContours(imgs,contours,-1,(0,0,255),2)
    return imgs
#imgsvis=seedvis(contours,seedimg,seedis,imgs)   

#绘制显示
def seedshow(imgs,l=640,w=480):
    cv.namedWindow("img",0);
    cv.resizeWindow("img", l, w);
    cv.imshow("img", imgs)    
    cv.waitKey(0)
#seedshow(imgsvis)    


def seedmea(pathwjj):
    start=time.time()
    
    #设置路径
    path = pathwjj#图片路径
    #path = r"F:\seed\0-10"#test
    #保存路径
    pathnor = os.path.join(path,"seednormal")
    if not os.path.exists(pathnor):
        os.makedirs(pathnor)#不存在路径则创建
    pathabn = os.path.join(path,"seedabnormal")
    if not os.path.exists(pathabn):
        os.makedirs(pathabn)
    global pathcsv#定义为全局变量
    pathcsv = os.path.join(path,"csv")
    if not os.path.exists(pathcsv):
        os.makedirs(pathcsv)
    #图片序列   
    imgsqall = [i for i in os.listdir(path)]#照片名称序列
    imgsq=[]
    for i in imgsqall:# 循环读取路径下的文件并筛选输出  
        if os.path.splitext(i)[1] == ".jpg":
            imgsq.append(i)
                    
  
    imgparao=pd.DataFrame(columns = ["name","area", "cir", "lenth", "width", "sumlw", "ratio", "ste"])#原始所有参数
    seeddata = pd.DataFrame(columns = ["name","area", "cir", "lenth", "width", "sumlw", "ratio", "ste"]) #正常种子参数
    seedabn= pd.DataFrame(columns = ["name","area", "cir", "lenth", "width", "sumlw", "ratio", "ste"]) #异常种子参数
    nowTime = time.time()
    for i in imgsq:
        curTime =time.time()
        if curTime - nowTime >= 1800:#每三秒输出一次执行
           print("执行"+str(i))
           nowTime=curTime
#读取图片
        im=os.path.join(path, i)
        imgs = cv.imread(im) 
        contours=canny_demo(imgs,t=200,e=2)#函数canny_demo  识别轮廓
        seedimg,lenth,scale_index=conparam(contours)#函数conparam  比例尺设为2,计算contours所有轮廓参数
        seedimg=seedimg.reindex(columns =["name","area", "cir", "lenth", "width", "sumlw", "ratio", "ste"], fill_value = str(i[:-4]))#添加列
        imgparao=imgparao.append(seedimg)#保存原始轮廓数据
        #获取所需数据
        seed,seedis=seedr(seedimg,lenth,scale_index)#函数seedr  抽取种子参数和需标记的索引 长度大于2的轮廓抽取出来
        seed=seed.reindex(columns =["name","area", "cir", "lenth", "width", "sumlw", "ratio", "ste"], fill_value = str(i[:-4]))#添加列
        imgsvis=seedvis(contours,seedimg,seedis,imgs)#函数seedvis  绘制外接框和标注

        if len(contours)<=30:
            #输出少轮廓数据
            seeddata=seeddata.append(seed)
            cv.imwrite(os.path.join(pathnor,i), imgsvis)#保存图片
        else:
            #输出多轮廓数据
            seedabn=seedabn.append(seed)
            cv.imwrite(os.path.join(pathabn,i), imgsvis)#保存图片
    
    imgparao.to_csv(os.path.join(pathcsv,'imgparao.csv'),index = None,encoding = 'utf8') #保存数据
    seeddata.to_csv(os.path.join(pathcsv,'seeddata.csv'),index = None,encoding = 'utf8') #保存数据
    seedabn.to_csv(os.path.join(pathcsv,'seedabn.csv'),index = None,encoding = 'utf8')    #保存数据

    end=time.time()
    print('Running time: %s Seconds'%(end-start))
    return imgparao,seeddata,seedabn


colorfile=namelist(r"F:\colorseed")

for i in colorfile:
    path=os.path.join(r"F:\colorseed",i)
#note 路径中不能包含中文
#    eximg=[]
    try:
        imgparao,seeddata,seedabn =seedmea(path)    
    except: 
#        eximg.append(str(i))
        print(str(i))
        print("有异常，程序继续运行")
#    eximg=pd.DataFrame(eximg)
#    eximg.to_csv(os.path.join(pathcsv,'eximg.csv'),index = None,encoding = 'utf8')

list=namelist(r"F:\colorseed\1\seedabnormal\acc")
