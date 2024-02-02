import cv2
cam = cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()
    width = cam.get(3)
    height = cam.get(4)

    if not ret:
        break

    frame_right_up = frame.copy()
    frame_down = frame.copy()

    frame_flipped_y_axis_to_top = cv2.flip(frame, 1)
    frame_flipped_x_axis_to_frame = cv2.flip(frame, 0)

    top_row = cv2.hconcat([frame, frame_flipped_y_axis_to_top])
    bottom_row = cv2.flip(top_row, 0)
    combined_frame = cv2.vconcat([top_row, bottom_row])

    cv2.imshow('MBS3523_Assignment_1bQ3', combined_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
