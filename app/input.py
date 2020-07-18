import platform
import random
import time

import pygame
import threading
from rotary_encoder_driver import Driver


def run_in_thread(fn):
    def run(*k, **kw):
        t = threading.Thread(target=fn, args=k, kwargs=kw)
        t.start()
        return t  # <-- this is new!

    return run


# Interfacing with the Keyboard API
class Keyboard(object):
    def __init__(self, channel):
        # init the linked stream
        self.channel = channel

        # init key values
        self.keys = [True] * 24

        # init digital knobs
        # change to arrow keys on mac
        self.digital_counter = [0] * 4
        self.digital_buffer = [0] * 4
        self.digital_driver = Driver(self.digital_buffer, scalar=True, factor=1)
        self.update_digital_counter()

        # Record button

        # Play button

        # Shift button

        # left right arrow

    # Change the channel we're connected
    def set_channel(self, channel):
        self.channel = channel

    @run_in_thread
    def update_digital_counter(self):
        if platform.system() == 'Darwin':
            self.digital_driver.start_mac_tester()
        else:
            self.digital_driver.start_driver()

    # controls the keyboard to hit a key
    def key_down(self, key_index):
        if self.keys[key_index]:
            # toggle key
            self.keys[key_index] = False
            # play note
            self.channel.key_down(key_index)

            self.digital_driver.set_factor(2)

    # controls the keyboard to release a key
    def key_up(self, key_index):
        # if is falling edge
        if not self.keys[key_index]:
            # toggle key
            self.keys[key_index] = True
            # play note
            self.channel.key_up(key_index)

    # gets the scroll of the digital knob
    def get_knob(self, knob_num):
        # if the digital_buffer changes
        if self.digital_buffer[knob_num] != self.digital_counter[knob_num]:
            # send the new value and update
            self.digital_counter[knob_num] = self.digital_buffer[knob_num]
            return self.digital_counter[knob_num]

        # if the digital_buffer is still the same return false
        return False

    # gets the scroll of the digital knob
    def get_knobs(self):
        knobs = [False] * 4
        # Update all 4 knobs
        for knob_num in range(4):
            # if the digital_buffer changes
            if self.digital_buffer[knob_num] != self.digital_counter[knob_num]:
                # send the new value and update
                self.digital_counter[knob_num] = self.digital_buffer[knob_num]
                knobs[knob_num] = self.digital_counter[knob_num]

        return knobs

    def use_knob(self, knob_num):
        self.channel.use_knob(knob_num=knob_num, index=self.digital_counter[knob_num])
