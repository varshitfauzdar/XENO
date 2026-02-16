import cv2
import pyautogui
import time
from hand_tracker import HandTracker
from gesture_controller import GestureController
from utils import fingers_up

# Open Camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera not detected")
    exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

tracker = HandTracker()

screen_w, screen_h = pyautogui.size()
controller = GestureController(screen_w, screen_h)

control_mode = False
toggle_cooldown = 0

# Create window and keep on top
cv2.namedWindow("XENO - Advanced Control", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("XENO - Advanced Control",
                      cv2.WND_PROP_TOPMOST,
                      1)

while True:
    success, frame = cap.read()

    if not success:
        print("Frame not captured")
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    landmarks = tracker.get_landmarks(frame)

    if landmarks:
        fingers = fingers_up(landmarks)
        x, y = landmarks[8][1], landmarks[8][2]

        # Toggle XENO ON/OFF (All fingers up)
        if fingers == [1, 1, 1, 1] and time.time() - toggle_cooldown > 1:
            control_mode = not control_mode
            toggle_cooldown = time.time()

        if control_mode:
            # Move cursor (index finger up)
            if fingers[0] == 1:
                controller.move_cursor(x, y, w, h)

            # Left click (index + middle)
            if fingers == [1, 1, 0, 0]:
                controller.left_click()

            # Right click (3 fingers)
            if fingers == [1, 1, 1, 0]:
                controller.right_click()

            # Drag (fist)
            if fingers == [0, 0, 0, 0]:
                controller.drag(x, y, w, h)

        # Draw fingertip indicator
        cv2.circle(frame, (x, y), 8, (0, 255, 0), -1)

    # Display control mode
    status = "ON" if control_mode else "OFF"
    color = (0, 255, 0) if control_mode else (0, 0, 255)

    cv2.putText(frame, f"XENO: {status}",
                (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                color,
                2)

    cv2.imshow("XENO - Advanced Control", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key == 27:
        break

cap.release()
cv2.destroyAllWindows()
