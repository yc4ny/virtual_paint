import cv2
import numpy as np

#WebCam Import
frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3,frameWidth)
cap.set(4,frameHeight)
cap.set(10,150) #Brightness

#Defining a list of colors, from colorpicker.py found the h,s,v values of the "red" stapler as
# l_h: 83, l_s: 126, l_v:53, h_h: 179, h_s: 200, h_v : 233
myColors = [83,126,53,179,200,233] #RED
myColorValues = [0,0,255] #BGR Format not RGB. From RGB color code chart found Red as 255,0,0

myPoints = []

#Function to find color
def findColor(img,myColors, myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newPoints=[]
    #A Generic Way of Detecting Color By Color
    lower = np.array([myColors[0], myColors[1], myColors[2]])
    upper = np.array([myColors[3], myColors[4], myColors[5]])
    mask = cv2.inRange(imgHSV, lower, upper)

    #Draws a circle at the Bound Box of the Object
    x,y = getContours(mask)
    cv2.circle(imgResult, (x,y), 10, (0,0,255), cv2.FILLED)
    if x!=0 and y !=0:
        newPoints.append([x,y,count])
        count +=1
    #cv2.circle(imgResult, (x, y), 10, myColorValues[count], cv2.FILLED)
    return newPoints

def getContours(img):
    x,y,w,h = 0,0,0,0
    #Finding outer corners
    contours,hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        #Drawing border/corner lines
        #cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 1)
        perimeter = cv2.arcLength(cnt, True)
        #Points of the corner points of each of the shapes
        approx = cv2.approxPolyDP(cnt, 0.02*perimeter, True)
        x, y, w, h = cv2.boundingRect(approx)
#Gives Center of the Bounding Box
    return x+w //2, y

def drawOnCanvas(myPoints, myColorValues):
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]),10, [0,0,255], cv2.FILLED)

while True:
    success, img = cap.read()
    imgResult = img.copy()
    newPoints = findColor(img, myColors, myColorValues)

    #For newpoint list append to each of elements
    if len(newPoints) != 0:
        for newP in newPoints:
            myPoints.append(newP)
    if len(myPoints)!=0:
        drawOnCanvas(myPoints,myColorValues)

    cv2.imshow("Result",imgResult)
    if cv2.waitKey(1) & 0Xff == ord('q'):
        break

