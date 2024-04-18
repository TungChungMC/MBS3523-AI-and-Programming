import cv2
import numpy as np
import serial

# Predefined HSV range for purple color
default_lowH, default_lowS, default_lowV = 120, 50, 50
default_highH, default_highS, default_highV = 150, 255, 255

# Initialize serial communication with Arduino
ser = serial.Serial('COM11', 115200)  # Change 'COM11' to the appropriate serial port

# Function to update HSV values based on trackbar positions
def update_HSV_values(lowH, lowS, lowV, highH, highS, highV):
    global new_lowH, new_lowS, new_lowV, new_highH, new_highS, new_highV
    new_lowH, new_lowS, new_lowV = lowH, lowS, lowV
    new_highH, new_highS, new_highV = highH, highS, highV

# Function to move camera servo based on centroid position
def move_camera_servo(centroid_x, centroid_y, frame_width, frame_height):
    panAngle = int(centroid_x * 180 / frame_width)  # Map centroid_x to 0-180 range
    tiltAngle = int(centroid_y * 180 / frame_height)  # Map centroid_y to 0-180 range
    panAngle = min(max(panAngle, 0), 180)  # Ensure panAngle is within 0-180 range
    tiltAngle = min(max(tiltAngle, 0), 180)  # Ensure tiltAngle is within 0-180 range
    ser.write(f"{panAngle},{tiltAngle}\r".encode())  # Send servo angles to Arduino
    print(f"Sent servo angles to Arduino: Pan={panAngle}, Tilt={tiltAngle}")

# Initialize webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Couldn't open webcam")
    exit()

# Create window for tuning HSV values
cv2.namedWindow("Tune HSV")
cv2.createTrackbar("LowH", "Tune HSV", default_lowH, 179, lambda x: None)
cv2.createTrackbar("HighH", "Tune HSV", default_highH, 179, lambda x: None)
cv2.createTrackbar("LowS", "Tune HSV", default_lowS, 255, lambda x: None)
cv2.createTrackbar("HighS", "Tune HSV", default_highS, 255, lambda x: None)
cv2.createTrackbar("LowV", "Tune HSV", default_lowV, 255, lambda x: None)
cv2.createTrackbar("HighV", "Tune HSV", default_highV, 255, lambda x: None)

while True:
    # Capture frame from webcam
    ret, frame = cap.read()
    if not ret:
        print("Error: Couldn't read frame")
        break

    # Convert frame from BGR to HSV color space
    hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Get current trackbar positions
    lowH = cv2.getTrackbarPos("LowH", "Tune HSV")
    highH = cv2.getTrackbarPos("HighH", "Tune HSV")
    lowS = cv2.getTrackbarPos("LowS", "Tune HSV")
    highS = cv2.getTrackbarPos("HighS", "Tune HSV")
    lowV = cv2.getTrackbarPos("LowV", "Tune HSV")
    highV = cv2.getTrackbarPos("HighV", "Tune HSV")

    # Update HSV values
    update_HSV_values(lowH, lowS, lowV, highH, highS, highV)

    # Define lower and upper bounds for the purple object in HSV
    lowerBound = np.array([new_lowH, new_lowS, new_lowV])
    upperBound = np.array([new_highH, new_highS, new_highV])

    # Threshold the HSV frame to get only the purple object
    mask = cv2.inRange(hsvFrame, lowerBound, upperBound)

    # Apply mask to the original frame
    result = cv2.bitwise_and(frame, frame, mask=mask)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # If contours are found, calculate centroid and adjust servos
    if contours:
        # Get largest contour
        largestContour = max(contours, key=cv2.contourArea)

        # Get bounding rectangle around the largest contour
        x, y, w, h = cv2.boundingRect(largestContour)

        # Draw rectangle around the detected object
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Calculate centroid of the largest contour
        centroid_x = x + w // 2
        centroid_y = y + h // 2

        # Move camera servo to track the purple object
        move_camera_servo(centroid_x, centroid_y, frame.shape[1], frame.shape[0])

    # Display the original frame with the purple object highlighted
    cv2.imshow("Original", frame)

    # Display the masked frame in the HSV tuning window
    cv2.imshow("Tune HSV", result)

    # Exit loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()