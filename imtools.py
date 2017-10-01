# -*- coding: utf8-*-
import cv2
from numpy import *

#车牌去除边框
def border_segment(src):
    w=src.shape[1]
    h=src.shape[0]
    flag=False
    pixels=0
    yy1=0
    yy2=h-1
  #  寻找上边界
    for y in xrange(h/2):
        curpixels=0
        for x in xrange(w):
            if src[y,x]==255:curpixels+=1
        if not flag:#上边界
            if (curpixels>pixels):pixels=curpixels
            if pixels-curpixels>0.6*pixels:#找到最上边的第一个空行
                flag=True
                pixels=curpixels
        else:
            if (curpixels<pixels):pixels=curpixels
            if curpixels-pixels>0.4*curpixels:#找到最上边的第一个字符行
                yy1=y#上边框位置
            #    print yy1
                flag=False
    
    #寻找下边界
    flag=False
    pixels=0
    for y in xrange(h-1,h/2-1,-1):#从下向上扫描
        curpixels=0
        for x in xrange(w):
            if src[y,x]==255:curpixels+=1
        if not flag:#上边界
            if (curpixels>pixels):pixels=curpixels
            if pixels-curpixels>0.6*pixels:#找到最下边的第一个空行
                flag=True
                pixels=curpixels
        else:
            if (curpixels<pixels):pixels=curpixels
            if curpixels-pixels>0.4*curpixels:#找到最下边的第一个字符行
                yy2=y#下边框位置
            #    print yy2
                flag=False
    #src[:yy1,:]=0
   # src[yy2:,:]=0#通过切片将边框以外的部分设置为黑色的点
    #寻找左边界
    xx1=0
    xx2=w-1
    flag=False
    pixels=0
    for x in xrange(w/8):
      #  print x
        curpixels=0
        for y in xrange(yy1,yy2):
            if src[y,x]==255:curpixels+=1
        if not flag:#左边界
            if (curpixels>pixels):pixels=curpixels
            if pixels-curpixels>0.7*pixels:#找到最左边的空列，此处参数越大表示值越近
                flag=True
                pixels=curpixels
        else:
            if (curpixels<pixels):pixels=curpixels
            if curpixels-pixels>0.3*curpixels:#找到第一个字符所在列，参数有待优化
                xx1=x#左边框位置
           #     print 'xx1:%s' % xx1
                flag=False
                
    #寻找右边界
    flag=False
    pixels=0
    for x in xrange(w-1,7*w/8-1,-1):#从右向左扫描
        curpixels=0
        for y in xrange(yy1,yy2):
            if src[y,x]==255:curpixels+=1
        if not flag:#左边界
            if (curpixels>pixels):pixels=curpixels
            if pixels-curpixels>0.6*pixels:#找到最右边的第一个空列
                flag=True
                pixels=curpixels
        else:
            if (curpixels<pixels):pixels=curpixels
            if curpixels-pixels>0.4*curpixels:#找到最右边的第一个字符列
                xx2=x#下边框位置
               # print 'xx2:%s' % xx2
                flag=False
    #src[:,:xx1]=0
    #src[:,xx2:]=0
    return src[yy1:yy2,xx1:xx2]
#车牌字符分割
def get_single_char(src):
    w=src.shape[1]
    h=src.shape[0]
    flag=False
    pixels=[]
    threshlod1=4#白色点数阈值，大于阈值为字符开始列，小于为字符结束列
    threshlod2=15#第一个汉字宽度阈值，必须要大于此阈值，才能被判定为完整的汉字
    for x in xrange(w):
        count=0
        for y in xrange(h):
            if src[y,x]==255:count+=1
        pixels.append(count)
    print pixels #打印所有列像素值为255的点数
    for x in xrange(w):#寻找第一个汉字
        count=0
        for y in xrange(h):
            if src[y,x]==255:count+=1
        if not flag and count>threshlod1:
            L=x
            flag=True
        if flag and count<threshlod1:
            R=x
            if R-L > threshlod2:break
    print L,R
    '''for y in xrange(h):
        src[y,L]=255
        src[y,R]=255'''
    flag=False
    Lborder=[]
    Rborder=[]
    threshlod2=12#剩下的六个字符间的宽度阈值
    for x in xrange(R+1,w):#寻找剩下的六个字符
        count=0
        for y in xrange(h):
            if src[y,x]==255:count+=1
        if not flag and count>threshlod1:
            xx1=x
            Lborder.append(xx1)
            print 'L:%s,count:%s' % (xx1,count)
            flag=True
        if flag and count<threshlod1:
            if x-xx1>threshlod2:
                xx2=x
                Rborder.append(xx2)
                print 'R:%s,count:%s' % (xx2,count)
                flag=False
    for y in xrange(h):
        for x in Lborder:
            src[y,x]=0
        for x in Rborder:
            src[y,x]=0
    #如果没有判断出最后一条边界，则将右边界加入到列表中
    if len(Rborder)<len(Lborder):Rborder.append(w-1)
    print Lborder,Rborder
    #字符归一化处理，5*10的尺寸
    char=[]#存储每个归一化后的图像列表
    char1=src[:,L:R]
    #print 'char1-11:',char1
    char1=cv2.resize(char1,(20,40))#resize 会改变一些像素点的值,会存在一些不为0或者255的点
    ret,char1=cv2.threshold(char1,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)#0-255
    cv2.imwrite('1.jpg' ,char1)
    #print 'char1:',char1
    for i in range(len(Lborder)):#处理剩下的六个字符
        char_each=src[:,Lborder[i]:Rborder[i]]
        char_each=cv2.resize(char_each,(20,40))
        ret,char_each=cv2.threshold(char_each,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        #进行细化
        '''kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(3,6))
        char_each=cv2.erode(char_each,kernel,iterations=2)'''
        #char_each=cv2Thin(char_each,1)
        cv2.imwrite('%s.jpg' % (i+2),char_each)
        #print char_each.shape,char_each[3,:]
        char.append(char_each)
    return char
    


