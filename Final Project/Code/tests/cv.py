import cv2
#import cv2.cv as cv
import numpy as np
import math

# Distance average for ball tracking
def average_distance(distance_list, length): 
    total = 0
    for i in distance_list:
        total += i
    return total / length
    
def average_defects(defects_list):
	return
	
	
    
# Ball tracking function
def ball_track():
    global mask_ball, ball_x, ball_rad, dist_x, dist_l, dist_r, dist_rad, dist_calc
    
    # blurred = cv2.medianBlur(frame, 13) # Much slower, include in report
    blurred = cv2.GaussianBlur(frame, (7, 7), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    mask_ball = cv2.inRange(hsv, lower_ball, upper_ball)
    mask_ball = cv2.erode(mask_ball, KERNEL_MORPH_BALL, iterations=2)
    mask_ball = cv2.dilate(mask_ball, KERNEL_MORPH_BALL, iterations=5)
    mask_ball = cv2.GaussianBlur(mask_ball,(11,11),0)

    # Detect circles using HoughCircles
    # param is threshold of size of circle
    # If param2 is low, more sensitive to small circles and false positive
    circles = cv2.HoughCircles(mask_ball,cv2.HOUGH_GRADIENT,2,120,param1=100,param2=40,minRadius=2,maxRadius=0)     

    #Draw Circles
    if circles is not None:
            for i in circles[0,:]:                
                ball_x.append(round(i[0])) # Append x center coordinate to list
                ball_rad.append(round(i[2])) # Append radius to list
                
                # Average every 5 entries
                if len(ball_x) == 5: 
                    dist_x = average_distance(ball_x, 5) # x coordinate of ball center
                    ball_x = []
                    
                    # Calculated distance of ball from camera
                    dist_rad = average_distance(ball_rad, 5) 
                    dist_calc = WIDTH_BALL * FOCAL / dist_rad
                    ball_rad = []
                    
                    # For output to control algorithm
                    dist_r = round(320 - (dist_x + dist_rad), 2)
                    dist_l = round(dist_x - dist_rad, 2)
                    
                    # Focal distance calculation
                    # focal = (dist_ave * 25.4 / 3.35) # in pixels and cm
                    
# Finger detection function
def hand_gesture():
    global mask_hand, finger, defects_list
    try:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)        

        # Get only glove color
        mask_hand = cv2.inRange(hsv, lower_hand, upper_hand)
        
        # Noise filtering
        mask_hand = cv2.GaussianBlur(mask_hand,(5,5),0)
        
        # Erosion and dilation (need to be adjusted)
        mask_hand = cv2.erode(mask_hand,KERNEL_MORPH_HAND,iterations = 1)
        mask_hand = cv2.dilate(mask_hand,KERNEL_MORPH_HAND,iterations = 2)
        
        # Noise filtering
        mask_hand = cv2.GaussianBlur(mask_hand,(5,5),0) 
     
        # Find contour
        contours,hierarchy= cv2.findContours(mask_hand,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        
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
            if angle < 90:
                defects_count += 1
        
        # Append defects count to list
        defects_list.append(defects_count)
        
        if len(defects_list) == 10:
            defects_most = max(defects_list,key=defects_list.count)
            defects_list = []
            # Finger print
            # 0 defect = finger 0 or 1
            if defects_most == 0:
                # If hull is 10% bigger than contour => finger 1
                if (area_hull-area_cnt)/(area_cnt) > .1: 
                    finger = 1
                else:
                    finger = 0
                 
            # 1 defect => finger 2
            elif defects_most == 1:
                finger = 2
            
            # 2 defects => finger 3
            elif defects_most == 2 :
                finger = 3
            
            # 3 defects => finger 4
            elif defects_most == 3:
                finger = 4
            
            # 4 defects => finger 5
            elif defects_most == 4:
                finger = 5

    except Exception:
        pass

# Constants
KERNEL_MORPH_BALL = np.ones((3,3),np.uint8)
KERNEL_MORPH_HAND = np.ones((4,4),np.uint8)
FOCAL = 220 # camera focal length
WIDTH_BALL = 3.35 # width of tennis ball

# HSV threshold of ball and hand
# Need to be adjusted depending on camera exposure and environment
# Glove HSV range
lower_hand = (110,109,12)
upper_hand = (120,255,84)
# Detect based on tennis ball color
lower_ball = (19, 91, 0)
upper_ball = (34, 255, 78)

# Take input from webcam
cap = cv2.VideoCapture(-1) # 640x480

# Reduce the size of video to 320x240 so rpi can process faster
cap.set(3,320)
cap.set(4,240)

# variables and list for functionalities
ball_x = [] # x axis coordinate of ball center
ball_rad = [] # Radius of ball center
dist_x = 0 # Pixel coordinate of ball center
dist_rad = 0 # Pixel radius of circle
defects_list = []

# Variables for modes and motor control
finger = 0 # Number for stop state
dist_calc = 0 # Distance of ball from camera in cm
dist_l = 0 # Pixel distance of circle from left of camera view
dist_r = 0 # Pixel distance of circle from right of camera view

while(1):

    _, frame = cap.read() # Read image frames from live video feed
    
    # Detect finger
    hand_gesture()
    #print(finger)

    # Track ball
    ball_track()
    print(dist_l,dist_r)
    
    # Display, should be removed when motor is implemented
    cv2.imshow('Hand mask',mask_hand)
    cv2.imshow('Ball mask',mask_ball)
    cv2.imshow('tracking',frame)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
