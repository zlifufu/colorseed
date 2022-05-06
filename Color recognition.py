# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 21:33:18 2022

@author: lifufu
"""


import  cv2
import numpy as np
import pandas as pd
from collections import Counter
import os 
import re
 
# 文字图片的路径
#只读取文件夹中图片
def list_jpg(path):
    dirr=os.listdir(path)
    dir1=[]
    for x in dirr:                             
        if os.path.splitext(x)[1] == ".jpg":   
            dir1.append(x)
    return dir1

#绘制显示
def seedshow(imgs,l=640,w=480):
    cv2.namedWindow("img",0);
    cv2.resizeWindow("img", l, w);
    cv2.imshow("img", imgs)    
    cv2.waitKey(0)
 
#绘制hsv
def drawhsv(h,s,v):
    #hsv空值
    img = np.ones((50,50),dtype=np.uint8)
    bgr_img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    hsv_img=cv2.cvtColor(bgr_img,cv2.COLOR_BGR2HSV) 
    #赋值HSV
    hsv_img[:,:,0] = h
    hsv_img[:,:,1] = s
    hsv_img[:,:,2] = v 
    bgr_img=cv2.cvtColor(hsv_img,cv2.COLOR_HSV2BGR)
    #seedshow(bgr_img,l=640,w=480) #BGR显示
    return bgr_img
'''
#背景条件选择
#杂色
backgroundimg =image[4][4];background2 =image[M-4][4];background3 =image[4][N-4];background4 =image[M-4][N-4]
a1=0.8 *backgroundimg[0];a2=1.2 *backgroundimg[0];b1=0.8 *backgroundimg[1];b2=1.2 *backgroundimg[1];c1=0.8 *backgroundimg[2];c2=1.2 *backgroundimg[2]
a12=0.8 *background2[0];a22=1.2 *background2[0];b12=0.8 *background2[1];b22=1.2 *background2[1];c12=0.8 *background2[2];c22=1.2 *background2[2]
a13=0.8 *background3[0];a23=1.2 *background3[0];b13=0.8 *background3[1];b23=1.2 *background3[1];c13=0.8 *background3[2];c23=1.2 *background3[2]
a14=0.8 *background4[0];a24=1.2 *background4[0];b14=0.8 *background4[1];b24=1.2 *background4[1];c14=0.8 *background4[2];c24=1.2 *background4[2]
  
Hcondition=((((Himage>a1)&(Himage<a2))|((Himage>a12)&(Himage<a22))|((Himage>a13)&(Himage<a23))|((Himage>a14)&(Himage<a24))),Himage)
Scondition=((((Simage>b1)&(Simage<b2))|((Simage>b12)&(Simage<b22))|((Simage>b13)&(Simage<b23))|((Simage>b14)&(Simage<b24))),Simage)
Vcondition=((((Vimage>c1)&(Vimage<c2))|((Vimage>c12)&(Vimage<c22))|((Vimage>c13)&(Vimage<c23))|((Vimage>c14)&(Vimage<c24))),Vimage)
condition=Hcondition[0]&Scondition[0]&Vcondition[0]
#白背景
Scondition=(Simage<21,Simage)
Vcondition=(Vimage>199,Vimage)
condition=Scondition[0]&Vcondition[0] 
#灰5
Scondition=(Simage<41,Simage)
Vcondition=(Vimage>149,Vimage)
condition=Scondition[0]&Vcondition[0] 
    #灰白背景
    Scondition=(Simage<41,Simage)
    Vcondition=(Vimage>149,Vimage)
    condition0=Scondition[0]&Vcondition[0]
    S1condition=(Simage<21,Simage)
    V1condition=(Vimage>129,Vimage)
    condition1=S1condition[0]&V1condition[0]
    S2condition=(Simage<11,Simage)
    V2condition=(Vimage>109,Vimage)
    condition2=S2condition[0]&V2condition[0]
    S3condition=(Simage<31,Simage)
    V3condition=(Vimage>139,Vimage)
    condition3=S3condition[0]&V3condition[0]
    S4condition=(Simage<9,Simage)
    V4condition=(Vimage>99,Vimage)
    condition4=S3condition[0]&V3condition[0]
    condition=condition1|condition0|condition2|condition3|condition4
#黑色背景
 Vcondition=(Vimage<30,Vimage)
    condition=Vcondition[0]
''' 
#提取种子颜色 像素原值  像素模糊image=image//10*10
def colorrecog(pic,imagepath,path_result):
    #读取图片转换为HSV    
    image = cv2.imread(imagepath,1)
    image = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    image=image//10*10
    #识别背景色 及其范围   
    M,N,d=image.shape
    
    #backgroundimg =image[4][4];background2 =image[M-4][4];background3 =image[4][N-4];background4 =image[M-4][N-4]
    #裁剪出图片中心25%作为识别颜色对象 去除比例尺颜色
    imagecut=image[int(0.25*M):int(0.75*M),int(0.25*N):int(0.75*N)]
    #定义HSV白色 
    #white=np.array([0,0,255])
    #green=np.array([60,150,150])
    #拆分三通道
    Himage=imagecut[:,:,0]
    Simage=imagecut[:,:,1]
    Vimage=imagecut[:,:,2]
    #背景色修改 HSV同时满足背景条件
    #Hcondition=((((Himage>a1)&(Himage<a2))|((Himage>a12)&(Himage<a22))|((Himage>a13)&(Himage<a23))|((Himage>a14)&(Himage<a24))),Himage)
    #黑色背景
    #Hcondition=(Himage<51,Himage)
    #Scondition=(Simage<51,Simage)
    Vcondition=(Vimage<51,Vimage)
    condition=Vcondition[0]#&Scondition[0]&Hcondition[0]
    #修改像素
    Himage=np.where(condition,60, Himage)
    Simage=np.where(condition,150, Simage)
    Vimage=np.where(condition,150, Vimage)
    #合并三通道H S V
    imageR=np.array([Himage,Simage,Vimage])
    imageR=imageR.swapaxes(0,2)
    imageR=imageR.swapaxes(0,1)
    imagecut=imageR#重新赋值
    #提取种子像素
    notcondition=~condition
    seedHimage=np.extract(notcondition,Himage)
    seedSimage=np.extract(notcondition,Simage)
    seedVimage=np.extract(notcondition,Vimage)
    #合成HSV列表
    #df1 = pd.DataFrame(list(seedHimage))#,seedSimage,seedVimage], columns=['a', 'b', 'c'])
    #df2 = pd.DataFrame(list(seedSimage))
    #df3 = pd.DataFrame(list(seedVimage))
    #df=pd.concat([df1, df2,df3], axis=1, join='outer')
    #seedpixel = df.apply(lambda x: tuple(x), axis=1).values.tolist()
    seedpixel = list(zip(seedHimage,seedSimage,seedVimage)) 
    #出现频率前300的像素
    seed_counter = Counter(seedpixel)
    seedcolor_counter300=seed_counter.most_common(300)
    
    #像素算术平均值
    a=np.array(seedpixel)
    seedcolor_mean=np.trunc(a.mean(axis=0))
    #显示提取非背景色效果
    #seedshow(imagecut,l=640,w=480) #hsv显示
    imagecut_BGR=cv2.cvtColor(imagecut,cv2.COLOR_HSV2BGR) 
    #seedshow(imagecut_BGR,l=640,w=480) #BGR显示
    #保存imagecut（提取非背景色效果）
    cv2.imwrite(os.path.join(path_result,pic[:-4]+"_e"+".jpg"), imagecut_BGR)#保存图片
    #显示众数颜色
    s=seedcolor_counter300[0][0]#众数的选择？ 
    H=s[0]
    S=s[1]
    V=s[2]
    bgr_img=drawhsv(H,S,V)
    #保存bgr_img（绘制的众数图）hsv格式不行，务必保存RGB格式
    cv2.imwrite(os.path.join(path_result,pic[:-4]+"_hsv"+".jpg"), bgr_img)#保存图片
    #seedscale.to_csv(os.path.join(path, 'seedscale.csv'),index = None,encoding = 'utf8')
    #seedscale.to_csv(os.path.join(path_result, 'seedscale.csv'),index = None,encoding = 'utf8')
    return str(s),str(seedcolor_counter300),str(seedcolor_mean)
    


import time
start = time.time()
try:
      #运行20个文件夹数据
    for i in range(3,4,1):
        print(i)
        path= os.path.join(r"F:/colorseed",str(i))
        path_result= os.path.join(r"F:/colorseed/result2colorrecognition",str(i))
        dir1 =list_jpg(path)
        listmost1=[]
        listmost300=[]
        listmean=[]
        for pic in dir1:
            imagepath= os.path.join(path,pic)
            most1,most300,mean=colorrecog(pic,imagepath,path_result)
            listmost1.append(most1)
            listmost300.append(most300)
            listmean.append(mean)
        seedcolors = pd.DataFrame({'img':dir1,'most1':listmost1,'most300':listmost300,'colormean':listmean}) 
        seedcolors.to_csv(os.path.join(path_result, 'seedcolors.csv'),index = None,encoding = 'utf8')       
except Exception as e:
    print(e)
    print(pic)
end = time.time() 
print(end-start)   
    




 #绘制hsv
def drawdrawhsv(h,s,v):
    #hsv空值
    img = np.ones((50,50),dtype=np.uint8)
    bgr_img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    hsv_img=cv2.cvtColor(bgr_img,cv2.COLOR_BGR2HSV) 
    #赋值HSV
    hsv_img[:,:,0] = h
    hsv_img[:,:,1] = s
    hsv_img[:,:,2] = v 
    bgr_img=cv2.cvtColor(hsv_img,cv2.COLOR_HSV2BGR)
    seedshow(bgr_img,l=640,w=480) #BGR显示
    return


drawdrawhsv(90,50,120)




imagepath=r"F:\colorseed\3\S0003084-1.jpg"
imagepath=r"F:\colorseed\result2colorrecognition\0\S0010304-1_e.jpg"
image = cv2.imread(imagepath,1)
image = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
image=image//10*10

imagecut=image
seedshow(imagecut,l=640,w=480)


















'''
快速删除文件夹
import shutil
shutil.rmtree(r"F:\colorseed\result2colorrecognition\3")
os.mkdir(r"F:\colorseed\result2colorrecognition\3")
#代码分析
lp = LineProfiler(colorrecog)
lp.runcall(colorrecog,pic,imagepath,path_result)
lp.print_stats()


#压缩array为元组    
a=np.array([1,2,3])
b=np.array([4,5,6])
c=np.array([7,8,9])
zipped = list(zip(a,b,c)) 

 
#提取种子颜色 像素原值  像素模糊image=image//10*10
def colorrecog(pic,imagepath,path_result):
    print("开始",time.time())
    #读取图片转换为HSV    
    image = cv2.imread(imagepath,1)
    image = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    image=image//10*10
    #识别背景色 及其范围   
    M,N,d=image.shape
    backgroundimg =image[4][4];background2 =image[M-4][4];background3 =image[4][N-4];background4 =image[M-4][N-4]
    a1=0.8 *backgroundimg[0];a2=1.2 *backgroundimg[0];b1=0.8 *backgroundimg[1];b2=1.2 *backgroundimg[1];c1=0.8 *backgroundimg[2];c2=1.2 *backgroundimg[2]
    a12=0.8 *background2[0];a22=1.2 *background2[0];b12=0.8 *background2[1];b22=1.2 *background2[1];c12=0.8 *background2[2];c22=1.2 *background2[2]
    a13=0.8 *background3[0];a23=1.2 *background3[0];b13=0.8 *background3[1];b23=1.2 *background3[1];c13=0.8 *background3[2];c23=1.2 *background3[2]
    a14=0.8 *background4[0];a24=1.2 *background4[0];b14=0.8 *background4[1];b24=1.2 *background4[1];c14=0.8 *background4[2];c24=1.2 *background4[2]
    #裁剪出图片中心25%作为识别颜色对象 去除比例尺颜色
    imagecut=image[int(0.25*M):int(0.75*M),int(0.25*N):int(0.75*N)]
    #定义HSV白色 
    #white=np.array([0,0,255])
    green=np.array([60,150,150])
    hight= imagecut.shape[0]
    width = imagecut.shape[1]
    #imagecut的将背景色替换为白色 提取非背景色至seedpixel
    seedpixel=[]
    print("参数准备",time.time())
    for row in range(hight):
        for col in range(width):
            j=imagecut[row,col]
            if (a1<j[0]<a2 and b1<j[1]<b2 and c1<j[2]<c2)\
            or (a12<j[0]<a22 and b12<j[1]<b22 and c12<j[2]<c22)\
            or (a13<j[0]<a23 and b13<j[1]<b23 and c13<j[2]<c23)\
            or (a14<j[0]<a24 and b14<j[1]<b24 and c14<j[2]<c24):
                imagecut[row,col]=green
            else:
                seedpixel.append(j)
    
    print("修改完成 ","种子颜色统计列表",time.time())
    #出现频率前300的像素
    c=[str(i) for i in seedpixel]
    seed_counter = Counter(c)
    seedcolor_counter300=seed_counter.most_common(300)
    #像素算术平均值
    a=np.array(seedpixel)
    seedcolor_mean=np.trunc(a.mean(axis=0))
    #显示提取非背景色效果
    #seedshow(imagecut,l=640,w=480) #hsv显示
    imagecut_BGR=cv2.cvtColor(imagecut,cv2.COLOR_HSV2BGR) 
    #seedshow(imagecut_BGR,l=640,w=480) #BGR显示
    #保存imagecut（提取非背景色效果）
    cv2.imwrite(os.path.join(path_result,pic[:-4]+"_e"+".jpg"), imagecut_BGR)#保存图片
    print("保存提取",time.time())
    #显示众数颜色
    s=seedcolor_counter300[0][0]#众数的选择？ 
    #s='[  001  40 210  ]' 案例
    s="["+s[1:-1].strip()+"]"#删除首尾空格
    s=' '.join(s.split())#去除连续空格
    douhao=','
    s=s.replace(" ",douhao)#，取代空格
    #提取数字至列表 解决"[02,181,124]"
    s = re.findall(r'\[(.*?)\]',s)#返回list
    s = s[0]
    s = s.split(',')
    s=[int(i) for i in s]
    #s=eval(s)#读取为列表 无法解决"[02,181,124]"
    H=s[0]
    S=s[1]
    V=s[2]
    bgr_img=drawhsv(H,S,V)
    #保存bgr_img（绘制的众数图）hsv格式不行，务必保存RGB格式
    cv2.imwrite(os.path.join(path_result,pic[:-4]+"_hsv"+".jpg"), bgr_img)#保存图片
    print("保存生成",time.time())
    #seedscale.to_csv(os.path.join(path, 'seedscale.csv'),index = None,encoding = 'utf8')
    #seedscale.to_csv(os.path.join(path_result, 'seedscale.csv'),index = None,encoding = 'utf8')
    return str(s),str(seedcolor_counter300),str(seedcolor_mean)




数组布尔运算
cond1=np.array([True,False,True,True,False])
cond2=np.array([False,True,True,True,False])
cond1&cond2


arr=np.array([[1,2,3],[4,5,6],[7,8,9]])
#定义条件,（元素 % 2==0）
A = np.array([5, 9, 11, 4, 31, 27,8])
condition=(~(((A>=3)&(A<8))|((A>=25)&(A<32))), arr)
print(condition[0])
print(np.extract(condition[0],A))
np.extract()

np.where(~(((A>=3)&(A<8))|((A>=25)&(A<32))), 0, A)#修改

print(np.extract(condition,x))



flag="[02,181,124]"
import re
flag = re.findall(r'\[(.*?)\]',flag)#返回list
print(flag)
flag = flag[0]
flag = flag.split(',')
print(flag)
flag1=[int(i) for i in flag]
int(flag)


imagepath = r"F:\seed\1_20000-result\S0005104-1.jpg"
imagepath = r"C:\Users\lifufu\Desktop\11111.jpg"

seed_counter,seedcolor_counter20,seedcolor_mean= colorrecog(imagepath)

drawhsv(18,125,169)
#自动生成文件夹
path_pic="F:\colorseed\结果2颜色识别"
for i in range(1,21,1):
    path1= os.path.join(path_pic,str(i))#需自动创建新acc
    if not os.path.exists(path1):

        



#提取种子颜色 像素原值
def colorrecog(pic,imagepath,path_result):
    #读取图片转换为HSV    
    image = cv2.imread(imagepath,1)
    image = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    #识别背景色 及其范围   
    backgroundimg =image[4][4]  
    a1=0.8 *backgroundimg[0]
    a2=1.2 *backgroundimg[0]
    b1=0.8 *backgroundimg[1]
    b2=1.2 *backgroundimg[1]
    c1=0.8 *backgroundimg[2]
    c2=1.2 *backgroundimg[2]
    #裁剪出图片中心25%作为识别颜色对象 去除比例尺颜色
    M,N,d=image.shape
    imagecut=image[int(0.25*M):int(0.75*M),int(0.25*N):int(0.75*N)]
    #定义HSV白色 
    white=np.array([0,0,255])
    hight= imagecut.shape[0]
    width = imagecut.shape[1]
    #imagecut的将背景色替换为白色 提取非背景色至seedpixel
    seedpixel=[]
    for row in range(hight):
        for col in range(width):
            j=imagecut[row,col]
            if a1<j[0]<a2 and b1<j[1]<b2 and c1<j[2]<c2:
                imagecut[row,col]=white
            else:
                seedpixel.append(j)
    
    #出现频率前300的像素
    c=[str(i) for i in seedpixel]
    seed_counter = Counter(c)
    seedcolor_counter300=seed_counter.most_common(300)
    #像素算术平均值
    a=np.array(seedpixel)
    seedcolor_mean=np.trunc(a.mean(axis=0))
    #显示提取非背景色效果
    #seedshow(imagecut,l=640,w=480) #hsv显示
    imagecut_BGR=cv2.cvtColor(imagecut,cv2.COLOR_HSV2BGR) 
    #seedshow(imagecut_BGR,l=640,w=480) #BGR显示
    #保存imagecut（提取非背景色效果）
    cv2.imwrite(os.path.join(path_result,pic[:-4]+"_e"+".jpg"), imagecut_BGR)#保存图片
    #显示众数颜色
    s=seedcolor_counter300[0][0] 
    s=' '.join(s.split())#去除连续空格
    s1=','
    s=s.replace(" ",s1)#，取代空格
    s=s[:1] + s[2:]  #去除第一个，
    #提取数字至列表 解决"[02,181,124]"
    s = re.findall(r'\[(.*?)\]',s)#返回list
    s = s[0]
    s = s.split(',')
    s1=[int(i) for i in s]
    #s=eval(s)#读取为列表
    H=s[0]
    S=s[1]
    V=s[2]
    bgr_img=drawhsv(H,S,V)
    #保存bgr_img（绘制的众数图）hsv格式不行，务必保存RGB格式
    cv2.imwrite(os.path.join(path_result,pic[:-4]+"_hsv"+".jpg"), bgr_img)#保存图片
    #seedscale.to_csv(os.path.join(path, 'seedscale.csv'),index = None,encoding = 'utf8')
    #seedscale.to_csv(os.path.join(path_result, 'seedscale.csv'),index = None,encoding = 'utf8')
    return str(s),str(seedcolor_counter300),str(seedcolor_mean)
'''

 


 


    
  


