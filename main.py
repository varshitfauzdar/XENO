import cv2
import pyautogui
from hand_tracker import HandTracker
from gesture_controller import GestureController
from utils import fingers_up

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

tracker = HandTracker()

screen_w, screen_h = pyautogui.size()
controller = GestureController(screen_w, screen_h)

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    landmarks = tracker.get_landmarks(frame)

    if landmarks:
        fingers = fingers_up(landmarks)
        x, y = landmarks[8][1], landmarks[8][2]

        # Move cursor
        if fingers[0] == 1:
            controller.move_cursor(x, y, w, h)

        # Pinch = Left click
        if fingers == [1, 1, 0, 0]:
            controller.left_click()

        # Three fingers = Right click
        if fingers == [1, 1, 1, 0]:
            controller.right_click()

        # Fist = Drag
        if fingers == [0, 0, 0, 0]:
            controller.drag(x, y, w, h)

        cv2.circle(frame, (x, y), 8, (0, 255, 0), -1)

    cv2.imshow("XENO - Gesture Control", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
