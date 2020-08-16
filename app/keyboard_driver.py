import platform
import pygame as pg
from rotary_encoder_driver import Driver
from threading_decorator import run_in_thread

KEYBOARD_BUTTON_LIST = [
    pg.K_z,  # C1
    pg.K_s,  # C#1
    pg.K_x,  # D1
    pg.K_d,  # D#1
    pg.K_c,  # E1
    pg.K_v,  # F1
    pg.K_g,  # F#1
    pg.K_b,  # G1
    pg.K_h,  # G#1
    pg.K_n,  # A1
    pg.K_j,  # A#1
    pg.K_m,  # B1
    pg.K_COMMA,  # C2
    pg.K_KP_0,  # C#2
    pg.K_KP_1,  # D2
    pg.K_KP_2,  # D#2
    pg.K_KP_3,  # E2
    pg.K_KP_4,  # F2
    pg.K_KP_5,  # F#2
    pg.K_KP_6,  # G2
    pg.K_KP_7,  # G#2
    pg.K_KP_8,  # A2
    pg.K_KP_9,  # A#2
    pg.K_KP_PLUS,  # B2
    pg.K_LSHIFT,  # Shift button
    pg.K_LEFT,  # left arrow
    pg.K_RIGHT,  # right arrow
    pg.K_RSHIFT,  # Record
    pg.K_BACKSPACE,  # Stop
    pg.K_RETURN,  # Play
    pg.K_9,  # Knob 1 up
    pg.K_o,  # Knob 1 down
    pg.K_0,  # Knob 2 up
    pg.K_p,  # Knob 2 down
    pg.K_MINUS,  # Knob 3 up
    pg.K_LEFTBRACKET,  # Knob 3 down
    pg.K_EQUALS,  # Knob 4 up
    pg.K_RIGHTBRACKET,  # Knob 4 down
]

FULL_KEYBOARD = [
    pg.K_z,  # C1
    pg.K_s,  # C#1
    pg.K_x,  # D1
    pg.K_d,  # D#1
    pg.K_c,  # E1
    pg.K_v,  # F1
    pg.K_g,  # F#1
    pg.K_b,  # G1
    pg.K_h,  # G#1
    pg.K_n,  # A1
    pg.K_j,  # A#1
    pg.K_m,  # B1
    pg.K_q,  # C2
    pg.K_2,  # C#2
    pg.K_w,  # D2
    pg.K_3,  # D#2
    pg.K_e,  # E2
    pg.K_r,  # F2
    pg.K_5,  # F#2
    pg.K_t,  # G2
    pg.K_6,  # G#2
    pg.K_y,  # A2
    pg.K_7,  # A#2
    pg.K_u,  # B2
    pg.K_LSHIFT,  # Shift button
    pg.K_LEFT,  # left arrow
    pg.K_RIGHT,  # right arrow
    pg.K_RSHIFT,  # Record
    pg.K_BACKSPACE,  # Stop
    pg.K_RETURN,  # Play
    pg.K_KP_7,  # Knob 1 up
    pg.K_KP_4,  # Knob 1 down
    pg.K_KP_8,  # Knob 2 up
    pg.K_KP_5,  # Knob 2 down
    pg.K_KP_9,  # Knob 3 up
    pg.K_KP_6,  # Knob 3 down
    pg.K_KP_MINUS,  # Knob 4 up
    pg.K_KP_PLUS  # Knob 4 down
]

COMPACT_KEYBOARD = [
    pg.K_z,  # C1
    pg.K_s,  # C#1
    pg.K_x,  # D1
    pg.K_d,  # D#1
    pg.K_c,  # E1
    pg.K_v,  # F1
    pg.K_g,  # F#1
    pg.K_b,  # G1
    pg.K_h,  # G#1
    pg.K_n,  # A1
    pg.K_j,  # A#1
    pg.K_m,  # B1
    pg.K_COMMA,  # C2
    pg.K_KP_0,  # C#2
    pg.K_KP_1,  # D2
    pg.K_KP_2,  # D#2
    pg.K_KP_3,  # E2
    pg.K_KP_4,  # F2
    pg.K_KP_5,  # F#2
    pg.K_KP_6,  # G2
    pg.K_KP_7,  # G#2
    pg.K_KP_8,  # A2
    pg.K_KP_9,  # A#2
    pg.K_KP_PLUS,  # B2
    pg.K_LSHIFT,  # Shift button
    pg.K_LEFT,  # left arrow
    pg.K_RIGHT,  # right arrow
    pg.K_RSHIFT,  # Record
    pg.K_BACKSPACE,  # Stop
    pg.K_RETURN,  # Play
    pg.K_UP,
    pg.K_DOWN,
    pg.K_SPACE,
    pg.K_9,  # Knob 1 up
    pg.K_o,  # Knob 1 down
    pg.K_0,  # Knob 2 up
    pg.K_p,  # Knob 2 down
    pg.K_MINUS,  # Knob 3 up
    pg.K_LEFTBRACKET,  # Knob 3 down
    pg.K_EQUALS,  # Knob 4 up
    pg.K_RIGHTBRACKET,  # Knob 4 down
]


# Interfacing with the Keyboard API
class Keyboard(object):
    def __init__(self, event_handler):
        # initialize with handler
        self.event_handler = event_handler

        # init key values
        self.key_dict = self.make_key_mapping()

        self.on_keys = set()

        # init digital knobs
        # change to arrow keys on mac
        self.encoder_counter = [0] * 4
        self.encoder_buffer = [0] * 4
        self.encoder_driver = Driver(self.encoder_buffer, scalar=True, factor=1)
        self.start_encoder_listener()

        # For tracking commonly used keys faster
        # Hard coded for faster access
        # Cannot be used for anything other than these functions
        self.shift = False

    # make list for piano keys
    @staticmethod
    def make_key_mapping():
        key_list = COMPACT_KEYBOARD
        mapping = {}
        for i in range(len(key_list)):
            mapping[key_list[i]] = (i)
        return mapping

    # Run encoder listener
    @run_in_thread
    def start_encoder_listener(self):
        if platform.system() == 'Darwin':
            self.encoder_driver.start_mac_tester()
        else:
            self.encoder_driver.start_driver()

    # get keyboard_dictionary value
    def get_key_index(self, key):
        return self.key_dict[key]

    def is_on(self, key):
        if key in self.on_keys:
            return True
        return False

    # -----------------
    # Control keyboard interface
    # -----------------

    # controls the keyboard to hit a key
    def key_down(self, key_index):
        # Checks the if the key is on and adds key to on keys if not on
        if key_index not in self.on_keys:
            # add key to on_notes
            self.on_keys.add(key_index)

            # play note
            self.event_handler.key_down(key_index)

            # Track shift button
            if key_index == 24:
                self.shift = True

    # controls the keyboard to release a key
    def key_up(self, key_index):
        if key_index in self.on_keys:
            # remove key from on_notes
            self.on_keys.remove(key_index)

            # play note
            self.event_handler.key_up(key_index)

            # Track record button
            if key_index == 24:
                self.shift = False

    # gets the scroll difference of the digital knob
    def get_knob(self, knob_num):
        # Gets the change of the knob
        difference = self.encoder_counter[knob_num] - self.encoder_buffer[knob_num]

        # if the digital_buffer changes
        if difference != 0:
            # send the new value and update
            self.encoder_counter[knob_num] = self.encoder_buffer[knob_num]
            return difference

        # if the digital_buffer is still the same return false
        return False

    # gets the scroll of the digital knob
    def append_to_queue(self, queue):
        # Update all 4 knobs
        for knob_num in range(4):
            # if the digital_buffer changes
            change = self.get_knob(knob_num)
            if change:
                queue.append((knob_num, change))
