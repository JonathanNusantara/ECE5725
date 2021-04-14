##################################################
#
# origin:  https://github.com/Sadaival/Hand-Gestures
#
##################################################
import traceback
import cv2
import numpy as np
import math


cap = cv2.VideoCapture(-1)

# Reduce the size of video to 320x240 so rpi can process faster
cap.set(3,320)
cap.set(4,240)
     
while(1):
        
    try:
        _, frame = cap.read()
        #frame=cv2.flip(frame,1)
        kernel = np.ones((4,4),np.uint8)
  
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)        
         
        # Glove HSV range
        lower_hand = (110,109,12)
        upper_hand = (120,255,84)
        
        # Get only glove color
        mask = cv2.inRange(hsv, lower_hand, upper_hand)
        
        # Noise filtering
        mask = cv2.GaussianBlur(mask,(5,5),0)
        
        # Erosion and dilation (need to be adjusted)
        mask = cv2.erode(mask,kernel,iterations = 1)
        mask = cv2.dilate(mask,kernel,iterations = 2)
        
        # Noise filtering
        mask = cv2.GaussianBlur(mask,(5,5),0) 
     
        # Find contour
        contours,hierarchy= cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        
        # Get max area in detected contour (which is the hand)
        area_max = 0
        contour_index = 0
        for i in range(len(contours)):
            cnt = contours[i]
            area_temp = cv2.contourArea(cnt)
            if area_temp > area_max:
                area_max = area_temp
                contour_index = i
        cnt = contours[contour_index]
        
        # Create convex hull of hand
        hull = cv2.convexHull(cnt)
                
        # Smooth and approximate the contour
        # http://creat-tabu.blogspot.com/2013/08/opencv-python-hand-gesture-recognition.html
        cnt_ap= cv2.approxPolyDP(cnt,0.0005*cv2.arcLength(cnt,True),True)

        # Calculate contour and hull area
        # To compare finger digit 0 or 1
        area_cnt = cv2.contourArea(cnt)
        area_hull = cv2.contourArea(hull)
        
        # Recalculate hull and calculate defects
        # Need returnPoints to be False
        hull = cv2.convexHull(cnt_ap, returnPoints=False)
        defects = cv2.convexityDefects(cnt_ap, hull)
        
        defects_count=0
        # Loop to find number of defects
        for i in range(defects.shape[0]):
            s,e,f,d = defects[i,0]
            start = tuple(cnt_ap[s][0])
            end = tuple(cnt_ap[e][0])
            far = tuple(cnt_ap[f][0])
            
            # Triangle lengths
            a = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
            b = math.sqrt((far[0] - end[0])**2 + (far[1] - end[1])**2)
            c = math.sqrt((start[0] - end[0])**2 + (start[1] - end[1])**2)

            # Distance between point and convex hull
            # Ideally not needed
            # s = (a+b+c)/2
            # ar = math.sqrt(s*(s-a)*(s-b)*(s-c))
            # d=(2*ar)/a

            # Calculate angle using cosine rule
            angle = math.acos((a**2 + b**2 - c**2) / (2 * a * b)) * 57.295
            
            # If angle <90, it is a defect caused by finger raised
            if angle <= 90:
                defects_count += 1
                cv2.circle(frame, far, 3, [255,0,0], -1)
            
            #draw lines around hand
            cv2.line(frame,start, end, [0,255,0], 2)
            
        defects_count+=1
        
        # Finger print
        font = cv2.FONT_HERSHEY_SIMPLEX
        if defects_count == 1:
            if (area_hull-area_cnt)/(area_cnt) > .1:
                cv2.putText(frame,'1',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
            else:
                cv2.putText(frame,'0',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
                
                    
        elif defects_count == 2:
            cv2.putText(frame,'2',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
            
        elif defects_count ==3 :
            cv2.putText(frame,'3',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
                    
        elif defects_count == 4:
            cv2.putText(frame,'4',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
            
        elif defects_count == 5:
            cv2.putText(frame,'5',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)

        #show the windows
        cv2.imshow('mask',mask)
        cv2.imshow('frame',frame)
    except Exception:
        traceback.print_exc()
        pass
       # break
        
    
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
    
cv2.destroyAllWindows()
cap.release()    
