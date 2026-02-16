import pyautogui
import time

pyautogui.FAILSAFE = False

class GestureController:
    def __init__(self, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.click_cooldown = 0

    def move_cursor(self, x, y, frame_w, frame_h):
        screen_x = self.screen_w * x / frame_w
        screen_y = self.screen_h * y / frame_h
        pyautogui.moveTo(screen_x, screen_y)

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
