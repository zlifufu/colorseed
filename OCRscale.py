# -*- coding: utf-8 -*-
"""
@author: lifufu
"""
import pytesseract
from PIL import Image
import os
import pandas as pd
import re

# 文字图片的路径

#只读取文件夹中图片
def list_jpg(path):
    dir=os.listdir(path)
    dir1=[]
    for x in dir:                             
        if os.path.splitext(x)[1] == ".jpg":   
            dir1.append(x)
    return dir1

#识别比例尺
path = r"F:\seed\0-10"
def scales(path,path_result):
    print("开始识别......")
    #scales_num = [pytesseract.image_to_string(os.path.join(path, i),lang="eng", config="--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789") for i in os.listdir(path)]#比例尺识别序列
    #加参数config="--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789"难以识别数字1  需要两次识别
    #识别稀疏字符psm 12
    scales_char = [pytesseract.image_to_string(os.path.join(path, i),lang="eng", config="--psm 12") for i in list_jpg(path)]#比例尺识别序列
    print("完成......")
    #小写去除scales_char空格和特殊字符
    scales_char1=[]
    for i in scales_char:
        a=i.lower()
        a=re.sub('\W+','', a)#去除空格和特殊字符
        scales_char1.append(a)
      
    #识别3mm/3cm   
    scales_char2=[]
    for i in scales_char1:  
        if "mm" in i:
            index=i.find("mm")
            scales=i[index-1:index+2]
            scales_char2.append(scales)
        elif "cm" in i:
            index=i.find("cm")
            scales=i[index-1:index+2]
            scales_char2.append(scales)
        else:
            scales="0"
            scales_char2.append(scales)
             
    imgs = [i[:-4] for i in list_jpg(path)]#照片名称序列 
    seedscale = pd.DataFrame({'imgs':imgs,'scales_char':scales_char,'scales_char1':scales_char1,'scales_char2':scales_char2}) 
    seedscale.to_csv(os.path.join(path, 'seedscale.csv'),index = None,encoding = 'utf8')
    seedscale.to_csv(os.path.join(path_result, 'seedscale.csv'),index = None,encoding = 'utf8')
    return scales_char2


#运行20个文件夹数据
for i in range(1,21,1):
    print(i)
    path= os.path.join(r"F:/colorseed",str(i))
    path_result= os.path.join(r"F:/colorseed/结果1",str(i))
    scale_char=scales(path,path_result) 


        
    
    
        
    

'''
print("识别完成......")
#比例尺字符串提取
scales1=[]
for i in scales:
    i=i.strip() 
    s=i.replace(" ", "")
    #s="".join(list(filter(str.isdigit, i)))
    if len(s)==0:
        s=999
    else:
        s
    scales1.append(s)
#比例尺数字提取    
scales2=[]
for i in scales:
    #s=i.strip()
    s="".join(list(filter(str.isdigit, i)))
    if len(s)==0:
        s=999
    else:
        s
    scales2.append(s)
seedscale = pd.DataFrame({'imgs':imgs,'scales':scales1,'digit':scales2}) 
print("数据整理完成......")
seedscale.to_csv('seedscale.csv',index = None,encoding = 'utf8') 
print("已导出结果")



import pytesseract
from PIL import Image
# 读取图片
im = Image.open(r"F:\seed\seed2.jpg")
# 识别文字
string = pytesseract.image_to_string(im)
print(string)

# 获取图片路径列表
imgs = [i for i in os.listdir(path)]#合并路径的正确方式join  os.path.join

# 打开文件
f = open('seedtext.txt', 'w+', encoding='utf-8')
# 将各个图片的路径写入text.txt文件当中
for img in imgs:
    f.write(img + '\n')
# 关闭文件
f.close()
# 文字识别
string = pytesseract.image_to_string('seedtext.txt')
print(string)
'''


