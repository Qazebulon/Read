#! /usr/bin/python3
# /words/mp3/p13.pt  ->  usb:Don2022 /tutor/read/p13.py
# MP3 Sound files from https://www.texttovoice.online/ (Salli, Female, ~45-70% speed)
#-----------------------------------------------------------------------------------------
#Pygame setup: [Making Games with Python & Pygame, pp. 8-12]
from random import randint
import pygame, sys, os
from pygame.locals import *
pygame.init()
DisplaySurface = pygame.display.set_mode((1000, 700))
pygame.display.set_caption('Reading Tutor')
#-----------------------------------------------------------------------------------------
# Enter Book Coode:							***** (0 / 3)
fileFound = False
while (fileFound == False):
    psetName = input("Enter Problem Set Code: ")	# Slect Problem Set (GEAH)
    psetFile = 'R1_'+psetName+'_0'
    try:						# Check if existing file Found
        f = open(psetFile, 'r')
        f.close()
        fileFound = True
    except IOError:
        fileFound = False
        print('Poblem Set Not Found')
#-----------------------------------------------------------------------------------------
# Log student in:							*****	(1 / 3)
newStudent = False
fileFound = False
while ((fileFound == False) and (newStudent==False)):
    studentName = input("Enter Student's Name: ")	# Get Student's Infornation
    fileName = 'R1_'+psetName+'_'+studentName
    try:						# Check if existing file Found
        f = open(fileName, 'r')
        f.close()
        fileFound = True
    except IOError:
        fileFound = False
        answ = input('New Student? (y/n): ')
        if ((answ=='y') or (answ=='Y')):
            newStudent=True
#------------------------------------------------------------------------------------------
# Define Colors:
BLACK=(0,0,0)
GRAY=(128,128,128)
WHITE=(255,255,255)
RED=(255,0,0)
YELLOW=(255,255,0)
GREEN=(0,128,0)
BLUE=(0,0,255)
VIOLET=(0,255,255)
#------------------------------------------------------------------------------------------
# 0) Problem Setup:
# load the words into an array: [Python3 Sams Python for Pi in 24 Hurs (music pp.517-521)]
# create word array: lists all words in nominal presentation order ("count" all worrds)
# create a probability array holding the starting (maximum) probability for each word
# create an eight-to-the-nth arraay
#------------------------------------------------------------------------------------------
f1=open(psetFile)
words=[]        # words
prob=[]         # probabilities (for each word)
count=0         # problem count
for l1 in f1:
    l2=l1[:-1]  # strip final character
    words.append(l2)	# 0A) append to words array
    prob.append(5)	# 0B) append "5" (always) to probability array
    count=count+1			# ***** "count" = total pproblems in full set *****
f1.close()
exp8 = (1,8,64,512,4096,32768)	# 0C) 8^N array: exp8[n]
#------------------------------------------------------------------------------------------
# Load Old-Student Data (if available -- into probability array)	*****	(2 / 3)
if (not newStudent):
        prob = []
        f = open(fileName, 'r')
        for line in f:
                prob.append(int(line))	    #(sys.stdout.write(line) # (like end='') Test)
        f.close()
#------------------------------------------------------------------------------------------
# Problem Run Loop:
#  Pygame runloop: [Making Games with Python & Pygame, pp. 8-12]
index=-1
old=0
while True: # Main Loop
    #--------------------------------------------------------------------------------------
    # 1) calculate the maximum possible word
    max = 16384
    sum = 0
    n=0
    while ((sum <= max) and (n < count)):	# add probabilities until sum > randNum
        sum = sum + exp8[prob[n]]		# (look up each probability in exp8 able)
        n=n+1					# (watch for last problem)
    level = n				# ***** "level" is number of keys displayed *****
    # Normalize maax if necessary
    if (max > sum): max=sum
    #-------------------------------------------------------------------------------------
    # 2) select the problem
    randNum = randint(0,max)		# generate a random number and ...
    sum = 0				# use it to select a word from the word array
    n = 0
    #for plevel in (5,4,3,2,1,0):        # in descending probability (frequency),
    while ((sum <= randNum) and (n<level)):		# add until sum > randNum
        #    if (plevel == prob[n]):     # (add only if matching probability level ...
        sum = sum + exp8[prob[n]]	# (overlow problem w/0 level limit)
        n = n + 1 #Dies when this goese to 52
    if (old == n - 1):		# one more try if same as last one
        randNum = randint(0,max)		# generate a random number and ...
        sum = 0				# use it to select a word from the word array
        n = 0
        #for plevel in (5,4,3,2,1,0):        # in descending probability (frequency),
        while ((sum <= randNum) and (n<level)):		# add until sum > randNum
            #    if (plevel == prob[n]):     # (add only if matching probability level ...
            sum = sum + exp8[prob[n]]
            n = n + 1
    select = n - 1				# ***** "select" = chosen problem *****
    old = select
    #-------------------------------------------------------------------------------------
    # 3) "scramble" the key arrangement
    scram=[]                            # initiiate scrambled-key array, then ...
    for plevel in (5,4,3,2,1,0):        # in descending probability (frequency),
        for n in range (0,level):       # but within that, in normall order,
            if (plevel == prob[n]):     # (add only if matching probability level ...
                scram.append(n)         #  to constructed array)
    #-------------------------------------------------------------------------------------
    # 4) generate the accessible fraction of the keyboard
    DisplaySurface.fill(BLUE)
    FontObject = pygame.font.Font(None, 60)
    TextSurfaceObject = FontObject.render(fileName, True, WHITE, BLUE)
    TextRectObject = TextSurfaceObject.get_rect()
    TextRectObject.bottomright = (985,695)
    DisplaySurface.blit(TextSurfaceObject,TextRectObject)
    for n in range (0,level):
        FontObject = pygame.font.Font(None, 60)
        if (prob[scram[n]] == 0):
            BCOLOR = GREEN
        else:
            BCOLOR = BLACK
        TextSurfaceObject = FontObject.render(' '+words[scram[n]]+' ', True, BCOLOR, WHITE)
        TextRectObject = TextSurfaceObject.get_rect()
        #TextRectObject.center = (110 + (int(n/11))*192,40 + (n % 11) * 62)     # Columns
        TextRectObject.center = (110 + (n % 5)*192,40 + int(n / 5) * 62)        # Rows
        DisplaySurface.blit(TextSurfaceObject,TextRectObject)
#-------------------------------------------------------------------------------------
    # Echo loop:
    echo = True
    while (echo):
        # 5) speak the selected word
        index = select
        pygame.mixer.music.load ('w'+words[index]+'.wav')	# load sound
        pygame.mixer.music.play (0)				# play sound once
        #---------------------------------------------------------------------------------
        # 6) Events:  wait for mouse entry: lookup word index, using key index
        waiting = True
        while (waiting):
            for event in pygame.event.get():	# event loop
                if event.type == MOUSEBUTTONDOWN:
                    waiting = False
                    mousex, mousey = event.pos
                    #index = int((mousey-15)/62) + 11*int((mousex-15)/192)	# Columns
                    index = 5*int((mousey-15)/62) + int((mousex-15)/192)	# Rows
                    try:
                        mouselect = scram[index]     # "mouselect" = mouse-selected answer
                    except IndexError:
                          mouselect = level
                    ## Valid key?
                    if (mouselect<level):
                        echo = False
                        # Play sound tied to each key: [Sams Python for Pi  (pp.517-521)]
                        pygame.mixer.music.load ('w'+words[mouselect]+'.wav') # load sound
                        pygame.mixer.music.play (0)			 # play sound once
                        pygame.time.wait(1000)
                        #-----------------------------------------------------------------
                        # 7) check if randomly selected word matches the mouse selection
                        if (select == mouselect):
                            #-------------------------------------------------------------
                            # 8A) if they match, reduce the probability for that word
                            #     and loop back to step 1.
                            prob[mouselect]=prob[mouselect]-1
                            if (prob[mouselect]<0):
                                prob[mouselect]=0	# don't go below zero
                            #-------------------------------------------------------------
                            # 8B) ***** Reward Game Goes Here *****
                            #-------------------------------------------------------------
                        else:
                            #-------------------------------------------------------------
                            # 9) if they don't match, maximize both the randomly-&-mousee
                            #    selected probabilities & loop back to "1".
                            prob[mouselect] = 4
                            prob[select] = 5	# Actually, force the correct ansewr
                if event.type == QUIT:		# if "quit"
                    #---------------------------------------------------------------------
                    # save student's statistics:			*****	(3 / 3)
                    f=open(fileName, 'w')
                    for n in range(0,count):
                        f.write(str(prob[n])+'\n')
                    f.close
                    print('Updated')
                    #---------------------------------------------------------------------
                    pygame.quit()		# exiit program
                    sys.exit()
                pygame.display.update()		# update display
