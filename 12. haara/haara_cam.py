import cv2

cascPath = "/Users/Liya/anaconda3/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml"
eyePath = "/Users/Liya/anaconda3/Lib/site-packages/cv2/data/haarcascade_eye.xml"
smilePath = "/Users/Liya/anaconda3/Lib/site-packages/cv2/data/haarcascade_smile.xml"

faceCascade = cv2.CascadeClassifier(cascPath)
eyeCascade = cv2.CascadeClassifier(eyePath)
smileCascade = cv2.CascadeClassifier(smilePath)

font = cv2.FONT_HERSHEY_SIMPLEX
video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(200, 200),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]
        cv2.putText(frame, 'Face', (x, y), font, 2, (255, 0, 0), 5)

    smile = smileCascade.detectMultiScale(
        roi_gray,
        scaleFactor=1.16,
        minNeighbors=35,
        minSize=(25, 25),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    for (sx, sy, sw, sh) in smile:
        cv2.rectangle(roi_color, (sh, sy), (sx + sw, sy + sh), (232, 0, 0), 2)
        cv2.putText(frame, 'Smile', (x + sx, y + sy), 1, 1, (255, 165, 0), 1)

    eyes = eyeCascade.detectMultiScale(roi_gray)
    for (ex, ey, ew, eh) in eyes:
        cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 0, 255), 2)
        cv2.putText(frame, 'Eye', (x + ex, y + ey), 1, 1, (101, 0, 255), 1)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
