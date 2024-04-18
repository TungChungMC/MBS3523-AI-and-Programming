import serial
import cv2

ser = serial.Serial('COM10', 9600)

cv2.namedWindow("Sensor Data")

cap = cv2.VideoCapture(0)

while True:
    data = ser.readline().decode().strip()
    ret, frame = cap.read()

    cv2.putText(frame, data, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Sensor Data", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

ser.close()
cap.release()
cv2.destroyAllWindows()