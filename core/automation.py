import time
import threading
from pynput.keyboard import Controller, Key
from pygetwindow import getActiveWindow

from PyQt5.QtCore import QObject

class AutoJumpWorker(QObject):
    """
    A worker that simulates space key presses at a given interval.
    """
    def __init__(self, interval=1.0):
        super().__init__()
        self.interval = interval
        self.running = False
        self.thread = None
        self.keyboard = Controller()
        self.check_only_in_game = True

    def _is_game_window_active(self):
        active_window = getActiveWindow()
        return active_window and active_window.title == '驱入虚空'

    def _run(self):
        while self.running:
            if self._is_game_window_active() or not self.check_only_in_game:
                self.keyboard.press(Key.space)
                time.sleep(0.05) # Keep the press for a short duration
                self.keyboard.release(Key.space)
            # Adjust for the press duration
            sleep_time = self.interval - 0.05
            if sleep_time > 0:
                time.sleep(sleep_time)

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run)
            self.thread.daemon = True
            self.thread.start()

    def stop(self):
        if self.running:
            self.running = False
            if self.thread and self.thread.is_alive():
                # Don't join, as it might block the GUI thread if sleep is long
                pass
            self.thread = None

    def set_interval(self, interval):
        try:
            new_interval = float(interval)
            if new_interval >= 0.1: # Set a minimum interval
                self.interval = new_interval
        except (ValueError, TypeError):
            pass # Keep the old interval if the new one is invalid

class AutoSprintWorker(QObject):
    """
    A worker that simulates Ctrl key presses.
    """
    def __init__(self, interval=0.1):
        super().__init__()
        self.interval = interval
        self.running = False
        self.thread = None
        self.keyboard = Controller()
        self.check_only_in_game = True

    def _is_game_window_active(self):
        active_window = getActiveWindow()
        return active_window and active_window.title == '驱入虚空'
    
    def _run(self):
        while self.running:
            if self._is_game_window_active() or not self.check_only_in_game:
                self.keyboard.press(Key.ctrl)
                time.sleep(0.05) # Keep the press for a short duration
                self.keyboard.release(Key.ctrl)
            # Adjust for the press duration
            sleep_time = self.interval - 0.05
            if sleep_time > 0:
                time.sleep(sleep_time)

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run)
            self.thread.daemon = True
            self.thread.start()

    def stop(self):
        if self.running:
            self.running = False
            if self.thread and self.thread.is_alive():
                # Don't join, as it might block the GUI thread if sleep is long
                pass
            self.thread = None

    def set_interval(self, interval):
        try:
            new_interval = float(interval)
            if new_interval >= 0.1: # Set a minimum interval
                self.interval = new_interval
        except (ValueError, TypeError):
            pass # Keep the old interval if the new one is invalid
