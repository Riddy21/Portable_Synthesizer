from synth import Synth
from threading_decorator import run_in_thread

# Class for connecting synths with the keyboard or handling it with other players
class Player(object):
    def __init__(self, keyboard,channels=None):
        # initialize channels and the keyboard
        if channels is None:
            channels = []
        self.channels = channels
        self.keyboard = keyboard

        # Set the playback hanlder on the keyboard to be this one
        self.keyboard.set_player(self)

        # Set the current mode to none
        self.current_mode = None

    # Add a new channel and declare its playing mode
    def add_channel(self, mode, port, instr=0, reverb=0.3, gain=270):
        # Find the channel number
        channel_length = len(self.channels)

        # Make the synth and add it to channels
        synth = Synth(mode=mode, channel=channel_length, port=port, instr=instr, reverb=reverb, gain=gain)
        self.channels.append(synth)

        # set the current playing mode and send the synth to it
        if mode == 'freeplay':
            self.current_mode = Freeplay(synth, keyboard=self.keyboard)

    def key_down(self, index):
        self.current_mode.key_down(index)

    def key_up(self, index):
        self.current_mode.key_up(index)

    def use_knob(self, index, knob_num):
        if knob_num == 0:
            self.current_mode.use_knob(index, knob_num)

class Freeplay(object):
    def __init__(self, synth, keyboard):
        # channel set to the proper synth
        self.channel = synth

        # map each key to a function dictionary
        self.key_mappings = self.map_index2function()

        # Keybaord pointer
        self.keyboard = keyboard

    @staticmethod
    def map_index2function():
        key_list = [
            "noteC1",  # C1
            "noteC#1",  # C#1
            "noteD1",  # D1
            "noteD#1",  # D#1
            "noteE1",  # E1
            "noteF1",  # F1
            "noteF#1",  # F#1
            "noteG1",  # G1
            "noteG#1",  # G#1
            "noteA1",  # A1
            "noteA#1",  # A#1
            "noteB1",  # B1
            "noteC2",  # C2
            "noteC#2",  # C#2
            "noteD2",  # D2
            "noteD#2",  # D#2
            "noteE2",  # E2
            "noteF2",  # F2
            "noteF#2",  # F#2
            "noteG2",  # G2
            "noteG#2",  # G#2
            "noteA2",  # A2
            "noteA#2",  # A#2
            "noteB2",  # B2
            "shift",  # Shift
            "octave_down",  # left arrow
            "octave_up"  # right arrow
        ]

        return key_list

    def key_down(self, index):
        if index < 24:
            self.channel.key_down(index)
        elif self.key_mappings[index] == 'octave_up':
            # shift octave if possible
            if self.channel.octave_shift(1):
                # Check if there are any on notes
                for i in range(24):
                    if i in self.keyboard.on_keys:
                        # Release the key
                        self.channel.key_up(i-12)
                        self.channel.key_down(i)

        elif self.key_mappings[index] == 'octave_down':
            # shift octave if possible
            if self.channel.octave_shift(-1):
                # Check if there are any on notes
                for i in range(24):
                    if i in self.keyboard.on_keys:
                        # Release the key
                        self.channel.key_up(i + 12)
                        self.channel.key_down(i)

    def key_up(self, index):
        if index < 24:
            self.channel.key_up(index)

    def use_knob(self, index, knob_num):
        if knob_num == 0:
            self.channel.change_synth(index)