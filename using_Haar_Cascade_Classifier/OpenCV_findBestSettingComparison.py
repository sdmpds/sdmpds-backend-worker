# -*- coding: utf-8 -*-
"""
Kamil Morawiecki
'sdmms'
Pedagogical University of Cracov - student project
"""

import cv2


#import cascade classifier of human body
body_csc = cv2.CascadeClassifier('haarcascade_fullbody.xml')

#table with actual number of people on each test image detected and counted by human
nOfPeople = [ 13, 20, 19, 9, 35, 6, 7, 5, 17, 12, 2, 16, 12, 11, 18, 6, 10, 11, 5, 12 ]

#table for saving numbers of people detected by computer
nOfPeopleDetected = []

#table for saving best stetting
bestSettings = []


for i in range(1, 21):
    
    #import image and save as value returned by 'imread' function of OpenCV
    img = cv2.imread('test_images\image'+str(i)+'.jpg')
    
    #converting image to monochromatic color and saving as 'gray' variable
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    differences = []
    setValue = []
    
    
    diff = 9600
    bestSetting = 1
    peopleDetected = 0
    
    for j in range(1, 10):
        #detecting human bodies on image
        bodies = body_csc.detectMultiScale(gray, 1.1, j)
        #drawing rectangles on elements of image recognized as human body
        
        cnt = 0
        
        for (x,y,w,h) in bodies:
            cv2.rectangle(img, (x,y), (x+w,y+h), (64,255,64), 2)
            cnt = cnt + 1
        
        if diff > abs(cnt - nOfPeople[i-2]):
            diff = abs(cnt - nOfPeople[i-2])
            bestSetting = j
            peopleDetected = cnt
            
        
        
    bestSettings.append(bestSetting)
    nOfPeopleDetected.append(peopleDetected)    
       
        
        
        
    print("Image nr " + str(i) + ", nr of people detected: " + str(nOfPeopleDetected[i-2]) + " at setting: " + str(bestSettings[i-2]))
            
    #showing final result    
    cv2.imshow('img', img)
    cv2.waitKey(0)