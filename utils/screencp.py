import numpy as np
from Project.utils.grabscreen import grab_screen
from Project.utils.directkeys import PressKey,ReleaseKey,A,W,S,D
from matplotlib import pyplot as plt
import cv2
import time
import sys
import os

def draw_lines(img,lines):
    try:
        for l in lines:
            coords=l[0]
            cv2.line(img,(coords[0],coords[1]),(coords[2],coords[3]),[230,230,230],3)
    except:
        pass

def draw_circles(img,circles):
    try:
        for i in circles[0, :1]:
            # draw the outer circle
            cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # draw the center of the circle
            cv2.circle(img, (i[0], i[1]), 2, (0, 0, 255), 3)
            return [i[0],i[1]]
    except:
        pass
def straight():
    PressKey(W)
    ReleaseKey(A)
    ReleaseKey(D)

def left():
    PressKey(A)
    time.sleep(0.1)
    ReleaseKey(W)
    ReleaseKey(D)
    ReleaseKey(A)

def right():
    PressKey(D)
    time.sleep(0.1)
    ReleaseKey(A)
    ReleaseKey(W)
    ReleaseKey(D)

def calmdown():
    ReleaseKey(W)
    ReleaseKey(A)
    ReleaseKey(D)

def roi(img,vertices):
    # blank mask:
    mask = np.zeros_like(img)

    # filling pixels inside the polygon defined by "vertices" with the fill color
    cv2.fillPoly(mask, vertices, 255)

    # returning the image only where mask pixels are nonzero
    masked = cv2.bitwise_and(img, mask)
    return masked


def process_img(img):
    original_image=img
    processed_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300)
    processed_img = cv2.GaussianBlur(processed_img, (3,3), 0 )
    copy=processed_img
    vertices = np.array([[30, 240], [30, 140], [195, 140], [195, 240]])
    processed_img = roi(processed_img, np.int32([vertices]))
    verticesP = np.array([[30, 270], [30, 230], [197, 230], [197, 270]])
    platform = roi(copy, np.int32([verticesP]))
    #                       edges
    #lines = cv2.HoughLinesP(platform, 1, np.pi/180, 180,np.array([]), 3, 2)
    #draw_lines(processed_img,lines)
    #draw_lines(original_image,lines)

    #Platform lines
    #imgray = cv2.cvtColor(platform,cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(platform,127,255,0)
    im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(original_image, contours, -1, (0,255,0), 3)
    try:
        platformpos=contours[0][0][0]
    except:
        platformpos=[[0]]
    circles = cv2.HoughCircles(processed_img, cv2.HOUGH_GRADIENT, 1, 20,
                               param1=90, param2=5, minRadius=1, maxRadius=3)

    ballpos=draw_circles(original_image,circles=circles)

    return processed_img,original_image,platform,platformpos,ballpos
def main():

    for i in list(range(4))[::-1]:
        print(i+1)
        time.sleep(1)

    paused = False
    c=0
    last_time = time.time()

    while(True):
        if not paused:
            # 800x600 windowed mode
            screen = grab_screen(title='FCEUX 2.2.3: Arkanoid (USA)')
            #if c%10==0:
            #   print('Recording at ' + str((10 / (time.time() - last_time)))+' fps')
            #dd   last_time = time.time()
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)

            processed,original,platform,platformpos,ballpos=process_img(screen)
            #screen = cv2.resize(screen, (160,90))

            try:
                if (platformpos[0] - ballpos[0] > 0):
                    left()
                else:
                    right()
            except:
                pass

            cv2.imshow('window',original)
            #cv2.imshow('window',cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
main()
