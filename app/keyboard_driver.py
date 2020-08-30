import platform
import pygame as pg
from rotary_encoder_driver import Driver
from threading_decorator import run_in_thread

FULL_KEYBOARD = {
    pg.K_z: 0,  # C1
    pg.K_s: 1,  # C#1
    pg.K_x: 2,  # D1
    pg.K_d: 3,  # D#1
    pg.K_c: 4,  # E1
    pg.K_v: 5,  # F1
    pg.K_g: 6,  # F#1
    pg.K_b: 7,  # G1
    pg.K_h: 8,  # G#1
    pg.K_n: 9,  # A1
    pg.K_j: 10,  # A#1
    pg.K_m: 11,  # B1
    pg.K_q: 12,  # C2
    pg.K_2: 13,  # C#2
    pg.K_w: 14,  # D2
    pg.K_3: 15,  # D#2
    pg.K_e: 16,  # E2
    pg.K_r: 17,  # F2
    pg.K_5: 18,  # F#2
    pg.K_t: 19,  # G2
    pg.K_6: 20,  # G#2
    pg.K_y: 21,  # A2
    pg.K_7: 22,  # A#2
    pg.K_u: 23,  # B2
    pg.K_LSHIFT: 'shift',  # Shift button
    pg.K_LEFT: 'left_arrow',  # left arrow
    pg.K_RIGHT: 'right_arrow',  # right arrow
    pg.K_RSHIFT: 'record',  # Record
    pg.K_BACKSPACE: 'stop',  # Stop
    pg.K_RETURN: 'play',  # Play
    pg.K_KP_7: 'knob_1_up',  # Knob 1 up
    pg.K_KP_4: 'knob_1_down',  #Knob 1 down
    pg.K_KP_8: 'knob_2_up',  # Knob 2 up
    pg.K_KP_5: 'knob_2_down',  # Knob 2 down
    pg.K_KP_9: 'knob_3_up',  # Knob 3 up
    pg.K_KP_6: 'knob_3_down',  # Knob 3 down
    pg.K_KP_MINUS: 'knob_4_up',  # Knob 4 up
    pg.K_KP_PLUS: 'knob_4_down'  # Knob 4 down
}

COMPACT_KEYBOARD = {
    pg.K_z: 0,  # C1
    pg.K_s: 1,  # C#1
    pg.K_x: 2,  # D1
    pg.K_d: 3,  # D#1
    pg.K_c: 4,  # E1
    pg.K_v: 5,  # F1
    pg.K_g: 6,  # F#1
    pg.K_b: 7,  # G1
    pg.K_h: 8,  # G#1
    pg.K_n: 9,  # A1
    pg.K_j: 10,  # A#1
    pg.K_m: 11,  # B1
    pg.K_COMMA: 12,  # C2
    pg.K_KP_0: 13,  # C#2
    pg.K_KP_1: 14,  # D2
    pg.K_KP_2: 15,  # D#2
    pg.K_KP_3: 16,  # E2
    pg.K_KP_4: 17,  # F2
    pg.K_KP_5: 18,  # F#2
    pg.K_KP_6: 19,  # G2
    pg.K_KP_7: 20,  # G#2
    pg.K_KP_8: 21,  # A2
    pg.K_KP_9: 22,  # A#2
    pg.K_KP_PLUS: 23,  # B2
    pg.K_LSHIFT: 'shift',  # Shift button
    pg.K_LEFT: 'left_arrow',  # left arrow
    pg.K_RIGHT: 'right_arrow',  # right arrow
    pg.K_RSHIFT: 'record',  # Record
    pg.K_BACKSPACE: 'stop',  # Stop
    pg.K_RETURN: 'play',  # Play
    pg.K_9: 'knob_1_up',  # Knob 1 up
    pg.K_o: 'knob_1_down',  # Knob 1 down
    pg.K_0: 'knob_2_up',  # Knob 2 up
    pg.K_p: 'knob_2_down',  # Knob 2 down
    pg.K_MINUS: 'knob_3_up',  # Knob 3 up
    pg.K_LEFTBRACKET: 'knob_3_down',  # Knob 3 down
    pg.K_EQUALS: 'knob_4_up',  # Knob 4 up
    pg.K_RIGHTBRACKET: 'knob_4_down',  # Knob 4 down
}

ONBOARD_KEYBOARD = {
    pg.K_z: 0,  # C1
    pg.K_RETURN: 1,  # C#1
    pg.K_x: 2,  # D1
    pg.K_PERIOD: 3,  # D#1
    pg.K_c: 4,  # E1
    pg.K_v: 5,  # F1
    pg.K_RIGHTBRACKET: 6,  # F#1
    pg.K_KP_1: 7,  # G1
    pg.K_RCTRL: 8,  # G#1
    pg.K_n: 9,  # A1
    pg.K_KP_5: 10,  # A#1
    pg.K_KP_0: 11,  # B1
    pg.K_KP_9: 12,  # C2
    pg.K_LEFTBRACKET: 13,  # C#2
    pg.K_END: 14,  # D2
    pg.K_LEFT: 15,  # D#2
    pg.K_DELETE: 16,  # E2
    pg.K_HOME: 17,  # F2
    pg.K_PAGEDOWN: 18,  # F#2
    pg.K_DOWN: 19,  # G2
    pg.K_6: 20,  # G#2
    pg.K_QUOTE: 21,  # A2
    pg.K_7: 22,  # A#2
    pg.K_BACKSPACE: 23,  # B2
    }

# Interfacing with the Keyboard API
class Keyboard(object):
    def __init__(self, event_handler):
        # initialize with handler
        self.event_handler = event_handler

        # init key values
        self.key_dict = ONBOARD_KEYBOARD

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
        self.record = False
        self.play = False

    # Run encoder listener
    @run_in_thread
    def start_encoder_listener(self):
        if platform.system() == 'Darwin':
            self.encoder_driver.start_mac_tester()
        else:
            self.encoder_driver.start_driver()

    # get keyboard_dictionary value
    def get_key_name(self, key):
        return self.key_dict[key]

    def is_on(self, key):
        if key in self.on_keys:
            return True
        return False

    # -----------------
    # Control keyboard interface
    # -----------------

    # controls the keyboard to hit a key
    def key_down(self, key_name):
        print(key_name)
        # Checks the if the key is on and adds key to on keys if not on
        if key_name not in self.on_keys:
            # add key to on_notes
            self.on_keys.add(key_name)

            # play note
            self.event_handler.key_down(key_name)

            # Track shift button
            if key_name == 'shift':
                self.shift = True
            elif key_name == 'record':
                self.record = True
            elif key_name == 'play':
                self.play = True

    # controls the keyboard to release a key
    def key_up(self, key_name):
        if key_name in self.on_keys:
            # remove key from on_notes
            self.on_keys.remove(key_name)

            # play note
            self.event_handler.key_up(key_name)

            # Track record button
            if key_name == 'shift':
                self.shift = False
            elif key_name == 'record':
                self.record = False
            elif key_name == 'play':
                self.play = False

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

    def use_knob(self, knob_num, change):
        self.event_handler.use_knob(knob_num, change)

    # gets the scroll of the digital knob
    def append_to_queue(self, queue):
        # Update all 4 knobs
        for knob_num in range(4):
            # if the digital_buffer changes
            change = self.get_knob(knob_num)
            if change:
                queue.append((knob_num, change))
