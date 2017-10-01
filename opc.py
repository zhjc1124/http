# -*- coding: utf8-*-
import cv2
import numpy as np
import imtools
import detect_plate

def split():
    img=cv2.imread('test.jpg')
    #img=cv2.imread('C:\Users\Administrator\Desktop\VC++数字图像处理\图像库\plate picture_jpg\Level_1\初出茅庐003.jpg')
    plate = detect_plate.detect(img)
    #开始下一步，进行字符分割
    plate=cv2.resize(plate,None,fx=2,fy=2) #放大两倍
    # cv2.imshow('2',plate)
    # cv2.waitKey(0)
    ret,img_binary=cv2.threshold(plate,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    #print 'img_binary-1:',img_binary[10,:]
    # print plate.shape
    jump=[]#存储每行0到255跳变的个数
    incline=False
    #进行倾斜检测
    for y in xrange(img_binary.shape[0]).__reversed__():#从下往上扫描，xrange返回的是列表
        # print y
         i=0
         for x in xrange(img_binary.shape[1]-1):#从左往右扫描,剔除最后一个元素
              if not img_binary[y,x] and img_binary[y,x+1]==255:
                   i+=1
         jump.append(i)
         if i>8 :
              if 3*jump[-1]/(jump[-2]+jump[-3]+jump[-4]) < 2.0 :
                   incline=True
              break
    #print jump
    #print img_binary[20]
    if incline:#倾斜校正,使用霍夫变换进行直线检测
         lines=cv2.HoughLines(img_binary.copy(),1,np.pi/180,128)#lines是一个三维数组
         #print lines
         all_line=sorted(lines,key=lambda line:line[0][0],reverse=True)#找到一条最长直线
        # print all_line
         max_line=all_line[0]
         aver_theta=0
         zzx = 0
         # print all_line
        # while(all_line[zzx][0]):
        #       aver_theta+=all_line[zzx][0]
        #       zzx = zzx + 1
        # aver_theta/=3  #取前三次最大的角度的平均值
         # print '倾斜角度为：%s' % np.rad2deg(np.pi/2-aver_theta)
         rho=max_line[0][0]
         theta=max_line[0][1]
         # 该直线与第一列的交点  
         pt1 = (0,int(rho/np.sin(theta)))  
         #该直线与最后一列的交点  
         pt2 = (img_binary.shape[1], int((rho-img_binary.shape[1]*np.cos(theta))/np.sin(theta)))  
    img_border=imtools.border_segment(img_binary)
    char=imtools.get_single_char(img_border)

