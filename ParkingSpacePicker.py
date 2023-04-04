import cv2 as cv
import pickle

# img = cv.imread('CarPark.png')

width = 135
height = 58
posList = []

try:
    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []

def mouseClick(events, x, y,flags, params):
    if events == cv.EVENT_LBUTTONDOWN:
        posList.append((x,y))

    if events == cv.EVENT_RBUTTONDOWN:
        for i,pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1+width and y1 < y < y1+height:
                posList.pop(i)

    with open('CarParkPos','wb') as f:
        pickle.dump(posList,f)

cap = cv.VideoCapture('CarPark.mp4')

while True:

    if cap.get(cv.CAP_PROP_POS_FRAMES) == cap.get(cv.CAP_PROP_FRAME_COUNT):
        cap.set(cv.CAP_PROP_POS_FRAMES, 0)

    success, img = cap.read()

    # cv.rectangle(img, (150, 133),(225, 167), (255,0,255), 3)
    # img = cv.imread('CarPark.png')
    for pos in posList:
        cv.rectangle(img,pos,(pos[0]+width , pos[1]+height), (255,0,255), 2)

    cv.imshow('Car Park', img)
    cv.setMouseCallback('Car Park', mouseClick)
    cv.waitKey(1)


