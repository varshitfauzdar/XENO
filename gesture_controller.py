import pyautogui
import time

pyautogui.FAILSAFE = False

class GestureController:
    def __init__(self, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.click_cooldown = 0

        # For smoothing
        self.prev_x = 0
        self.prev_y = 0
        self.smoothing = 5  # higher = smoother

    def move_cursor(self, x, y, frame_w, frame_h):
        screen_x = self.screen_w * x / frame_w
        screen_y = self.screen_h * y / frame_h

        # Smooth interpolation
        curr_x = self.prev_x + (screen_x - self.prev_x) / self.smoothing
        curr_y = self.prev_y + (screen_y - self.prev_y) / self.smoothing

        pyautogui.moveTo(curr_x, curr_y)

        self.prev_x = curr_x
        self.prev_y = curr_y

    def left_click(self):
        if time.time() - self.click_cooldown > 0.5:
            pyautogui.click()
            self.click_cooldown = time.time()

    def right_click(self):
        if time.time() - self.click_cooldown > 0.5:
            pyautogui.rightClick()
            self.click_cooldown = time.time()

    def drag(self, x, y, frame_w, frame_h):
        screen_x = self.screen_w * x / frame_w
        screen_y = self.screen_h * y / frame_h
        pyautogui.dragTo(screen_x, screen_y, button="left")
