
import cv2 as cv
import numpy as np
import pickle
import cvzone

cap = cv.VideoCapture('CarPark.mp4')

with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

width = 135
height = 58

def checkParkingSpace(imgPro):
    for pos in posList:
        x,y = pos
        # cv.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)
        imgCrop = imgPro[y:y+height, x:x+width]
        # cv.imshow(str(x*y), imgCrop)
        count = cv.countNonZero(imgCrop)
        cvzone.putTextRect(img,str(count),(x,y+height-10), scale = 1, thickness=1, offset=0)

        if count <1300:
            color = (0,255,0)
            thickness = 5
        else:
            color = (0,0,255)
            thickness =2

        cv.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)

while True:
    if cap.get(cv.CAP_PROP_POS_FRAMES) == cap.get(cv.CAP_PROP_FRAME_COUNT):
        cap.set(cv.CAP_PROP_POS_FRAMES, 0)

    success, img = cap.read()
    imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    imgBlur = cv.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv.adaptiveThreshold(imgBlur, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 25,16)
    imgMedian = cv.medianBlur(imgThreshold,5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv.dilate(imgMedian, kernel, iterations = 1)


    checkParkingSpace(imgDilate)
    # for pos in posList:
    #     cv.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)

    cv.imshow("Video", img)
    # cv.imshow('ImageBlur', imgBlur)
    # cv.imshow('ImageThreshold',imgThreshold)
    # cv.imshow('Median', imgMedian)
    cv.waitKey(10)
