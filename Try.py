import cv2
import imutils
import pytesseract
pytesseract.pytesseract.tesseract_cmd=r"C:\Program Files\Tesseract-OCR\tesseract.exe"
from time import sleep

key = cv2.waitKey(1)
webcam = cv2.VideoCapture(0)
sleep(2)
while True:

    check, frame = webcam.read()
    print(check)  # prints true as long as the webcam is running
    print(frame)  # prints matrix values of each framecd
    cv2.imshow("Capturing", frame)
    key = cv2.waitKey(1)
    if key == ord('s'):
        cv2.imwrite(filename='test.jpeg', img=frame)
        webcam.release()
        break
    elif key == ord('q'):
        webcam.release()
        cv2.destroyAllWindows()
        break
image = cv2.imread('test.jpeg')
image = imutils.resize(image,width=500)
cv2.imshow("Original Image",image)
cv2.waitKey(0)
gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
cv2.imshow("1- Grayscale Conversion",gray)
cv2.waitKey(0)
gray=cv2.bilateralFilter(gray,11,17,17)
cv2.imshow("2- Bilateral Filter",gray)
cv2.waitKey(0)
edges=cv2.Canny(gray,170,200)
cv2.imshow("3- Canny Edges",edges)
cv2.waitKey(0)
cnts,new=cv2.findContours(edges.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
img1=image.copy()
cv2.drawContours(img1,cnts,-1,(0,255,0),3)
cv2.imshow("4- All Contours",img1)
cv2.waitKey(0)
cnts=sorted(cnts,key=cv2.contourArea,reverse=True)[:10]
NumberPlateCnt=None
img2=image.copy()
cv2.drawContours(img2,cnts,-1,(0,255,0),3)
cv2.imshow("5- Top 10 Contours",img2)
cv2.waitKey(0)
count=0
idx=7
for c in cnts:
    peri=cv2.arcLength(c,True)
    approx=cv2.approxPolyDP(c,0.02*peri,True)
    if len(approx)==4:
        NumberPlateCnt=approx
        x,y,w,h=cv2.boundingRect(c)
        new_img=image[y:y+h,x:x+w]
        cv2.imwrite('Cropped image'+str(idx)+'.png',new_img)
        idx+=1
        break
cv2.drawContours(image,[NumberPlateCnt],-1,(0,255,0),3)
cv2.imshow("Final image ",image)
cv2.waitKey(0)
Cropped_img_loc='Cropped image7.png'
text=pytesseract.image_to_string(Cropped_img_loc,lang='eng')
print("Number is : ",text)
cv2.imshow("Number is: "+text,cv2.imread(Cropped_img_loc))
cv2.waitKey(0)