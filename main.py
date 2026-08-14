import cv2

camera = cv2.VideoCapture(0)

while True:
    sucesso, frame = camera.read()

    if not sucesso:
        break

    cv2.imshow("Webcam", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()