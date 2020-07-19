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
        self.keyboard.set_player(self)

        self.current_channel = None

    def add_channel(self, mode, port, instr=0, reverb=0.3, gain=270):
        channel_length = len(self.channels)
        synth = Synth(mode=mode, channel=channel_length, port=port, instr=instr, reverb=reverb, gain=gain)
        self.channels.append(synth)
        self.current_channel = synth

    def key_down(self, index):
        if self.current_channel.mode == 'freeplay':
            self.current_channel.key_down(index)

    def key_up(self, index):
        if self.current_channel.mode == 'freeplay':
            self.current_channel.key_up(index)

    def use_knob(self, index, knob_num):
        if self.current_channel.mode == 'freeplay':
            if knob_num == 0:
                self.current_channel.use_knob(index, knob_num)
