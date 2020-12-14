import cv2
import matplotlib.pyplot as plt

font = cv2.FONT_HERSHEY_SIMPLEX

cascPath = "/Users/Liya/anaconda3/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml"
eyePath = "/Users/Liya/anaconda3/Lib/site-packages/cv2/data/haarcascade_eye.xml"
smilePath = "/Users/Liya/anaconda3/Lib/site-packages/cv2/data/haarcascade_smile.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
eyeCascade = cv2.CascadeClassifier(eyePath)
smileCascade = cv2.CascadeClassifier(smilePath)

gray = cv2.imread('image.jpg', 0)
plt.figure(figsize=(12, 8))
plt.imshow(gray, cmap='gray')
plt.show()

faces = faceCascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    flags=cv2.CASCADE_SCALE_IMAGE

for (x, y, w, h) in faces:
    cv2.rectangle(gray, (x, y), (x + w, y + h), (255, 255, 255), 3)

plt.figure(figsize=(12, 8))
plt.imshow(gray, cmap='gray')
plt.show()
