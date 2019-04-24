# -*- coding: utf-8 -*-
"""
Kamil Morawiecki
'sdmms'
Pedagogical University of Cracov - student project
"""

import cv2

def findPeople(image_src):

    #import cascade classifier of human body
    body_csc = cv2.CascadeClassifier('haarcascade_fullbody.xml')
    
    
    #import image and save as value returned by 'imread' function of OpenCV
    img = cv2.imread(image_src)
        
    #converting image to monochromatic color and saving as 'gray' variable
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
    
    #detecting human bodies on image
    bodies = body_csc.detectMultiScale(gray, 1.1, 2)
    #drawing rectangles on elements of image recognized as human body
            
    cnt = 0
            
    for (x,y,w,h) in bodies:
        cv2.rectangle(img, (x,y), (x+w,y+h), (64,255,64), 2)
        cnt = cnt + 1
           
            
    print("Nr of people detected: " + str(cnt))
                
    #showing final result    
    cv2.imshow('img', img)
    cv2.waitKey(0)
    
    
    
    
#sample of calling function 'findPeople' for finding human bodies using Haar Cascade Classifier   
findPeople('test_images\image1.jpg')