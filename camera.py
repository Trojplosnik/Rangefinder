import cv2

cap = cv2.VideoCapture(0)


while True:
    ret, img = cap.read()

    cv2.imshow("camera", img)

    if cv2.waitKey(10) == 27:
        ret, frame = cap.read()
        cv2.imwrite('images/cam.png', frame)
        break

cap.release()
cv2.destroyAllWindows()
