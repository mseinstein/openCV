#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 20:14:05 2017

@author: bj
"""

import cv2
import os
#import numpy as np
import random
#import time
#from matplotlib import pyplot as plt
from playsound import playsound
from datetime import datetime
#import pygame
#pygame.mixer.init()


#os.chdir('/home/bj/github/openCV/rock_paper_scissors')
#os.chdir('E:\\GitHub\\openCV\\rock_paper_scissors')

# Rock paper Scissors 

cap = cv2.VideoCapture(0)

fist_cascade = cv2.CascadeClassifier('fist.xml')
palm_cascade = cv2.CascadeClassifier('palm.xml')
hand_cascade = cv2.CascadeClassifier('hand.xml')

font = cv2.FONT_HERSHEY_SIMPLEX
pc_opts = ['Rock','Paper','Scissors']
pc_play = ['']
hum_play = ['']
hum_choice = ['']

# Window size
frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Countdown 
nSecond = 0
totalSec = 3
strSec = '321'
startTime = 0.0
timeElapsed = 0.0
startCounter = False
outcome_check = 0

# Running scores
hum_score = 0
pc_score = 0
while(1):

    # Take each frame
    _, frame = cap.read()
    frame = cv2.flip(frame,1)
    
    # Convert BGR to Gray
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    
    
    
    # Locate faces
    fists = fist_cascade.detectMultiScale(gray, 1.3, 5)
    palms = palm_cascade.detectMultiScale(gray, 1.3, 5)
    hands = hand_cascade.detectMultiScale(gray, 1.3, 5)
    if len(hands) > 0:
        hum_play = ['Scissors']
    elif len(fists) > 0 :
        hum_play = ['Rock']
    elif len(palms) > 0 :
        hum_play = ['Paper']
    if not outcome_check:
        cv2.putText(frame,"Press S to start",(100,100), font, 2,(0,0,0),2,cv2.LINE_AA)
        
    cv2.putText(frame,hum_play[0],(100,200), font, 2,(255,255,255),2,cv2.LINE_AA)
        
    cv2.putText(frame,hum_choice[0],(100,425), font, 1,(255,0,0),2,cv2.LINE_AA)
    cv2.putText(frame,pc_play[0],(100,350), font, 1,(0,0,255),2,cv2.LINE_AA)
    cv2.putText(frame,"Humans: " + str(hum_score),(250,425), font, 1,(255,0,0),2,cv2.LINE_AA)
    cv2.putText(frame,"Computer: " + str(pc_score),(250,350), font, 1,(0,0,255),2,cv2.LINE_AA)
    
    # Display counter on screen before saving a frame
    if startCounter:
        if nSecond < totalSec: 
            # draw the Nth second on each frame 
            # till one second passes  
            cv2.putText(img = frame, 
                        text = strSec[nSecond],
                        org = (int(frameWidth/2 - 20),int(frameHeight/2)), 
                        fontFace = font, 
                        fontScale = 6, 
                        color = (255,255,255),
                        thickness = 5, 
                        lineType = cv2.LINE_AA)
            timeElapsed = (datetime.now() - startTime).total_seconds()
            if timeElapsed >= 1:
                nSecond += 1
                timeElapsed = 0
                startTime = datetime.now()
    if nSecond == totalSec:
        os.system("aplay Shoot.wav")
        #playsound('Shoot.mp3')
##        pygame.mixer.music.load('Shoot.mp3')
##        pygame.mixer.music.play()
##        while pygame.mixer.music.get_busy(): 
##            pygame.time.Clock().tick(10)
        nSecond = 0
        startCounter = False
        pc_play = random.sample(pc_opts,1)
        cv2.putText(frame,pc_play[0],(100,350), font, 1,(0,0,255),2,cv2.LINE_AA)
    
    # Outcome
    if pc_play != [''] and outcome_check:
        if hum_play[0] == 'Rock':
            os.system("aplay Rock.wav")
        elif hum_play[0] == 'Paper':
            os.system("aplay Paper.wav")
        elif hum_play[0] == 'Scissors':
            os.system("aplay Scissors.wav")



        
        if hum_play[0] == pc_play[0]:
            #playsound('It_is_a_tie.mp3')
            os.system("aplay Tie.wav")
            outcome = 'Tie'
        elif ((hum_play[0] == 'Rock' and pc_play[0] == 'Scissors') or 
            (hum_play[0] == 'Scissors' and pc_play[0] == 'Paper') or
            (hum_play[0] == 'Paper' and pc_play[0] == 'Rock')):
            #playsound('The_Human_Wins.mp3')
            os.system("aplay Hum_Win.wav")
            outcome = 'Human Wins'
            hum_score +=1
        elif ((pc_play[0] == 'Rock' and hum_play[0] == 'Scissors') or 
            (pc_play[0] == 'Scissors' and hum_play[0] == 'Paper') or
            (pc_play[0] == 'Paper' and hum_play[0] == 'Rock')):
            #playsound('The_Computer_Wins.mp3')
            #pygame.mixer.music.load('The_Computer_Wins.mp3')
            #pygame.mixer.music.play()
            #while pygame.mixer.music.get_busy(): 
            #    pygame.time.Clock().tick(10)
            os.system("aplay Comp_Win.wav")
            outcome = 'Computer Wins'
            pc_score +=1
        hum_choice = [hum_play[0]]
        cv2.putText(frame,outcome,(100,200), font, 4,(0,0,255),2,cv2.LINE_AA)
        outcome_check = 0
        

    
#    cv2.namedWindow("frame", cv2.WND_PROP_FULLSCREEN)          
#    cv2.setWindowProperty("frame", cv2.WND_PROP_FULLSCREEN, cv2.cv.CV_WINDOW_FULLSCREEN)
    cv2.imshow('frame',frame)

    k = cv2.waitKey(1) & 0xFF
    if k == 27 or k == ord('q'):
        break
    elif k == ord('s'):
        os.system("aplay Ready.wav")
        #playsound('Ready.mp3')
        #pygame.mixer.music.load('Ready.mp3')
        #pygame.mixer.music.play()
        #while pygame.mixer.music.get_busy(): 
        #    pygame.time.Clock().tick(10)
        startCounter = True      
        startTime = datetime.now()
        outcome_check = 1
        pc_play = ['']
#        keyPressTime = datetime.now()
#        pc_play = random.sample(pc_opts,1)
    
   
        
    

cv2.destroyAllWindows()
cap.release()
