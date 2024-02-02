import cv2

cam = cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()
    width = int(cam.get(3))
    height = int(cam.get(4))

    # Resize frame to one-fourth of its original size
    resized_frame = cv2.resize(frame, (width // 2, height // 2))

    frameCanny = cv2.Canny(resized_frame, 100, 300)
    frameHSV = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2HSV)
    frameBlur = cv2.GaussianBlur(resized_frame, (55, 55), 0)

    cv2.imshow("Webcam", resized_frame)
    cv2.imshow("Webcam Canny Edges", frameCanny)
    cv2.imshow("Webcam HSV", frameHSV)
    cv2.imshow("Webcam Gaussian Blur", frameBlur)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
