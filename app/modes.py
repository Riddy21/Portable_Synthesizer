# ------------------
# Mode controllers
# ------------------

# Parent object for all modes
import time
from synth import Synth


class Mode(object):
    def __init__(self, name, event_handler):
        self.current_channel_index = event_handler.current_channel_index

        self.name = name

        # Keybaord pointer
        self.keyboard = event_handler.keyboard

        # Playback handler pointer for switching modes
        self.event_handler = event_handler

        # Get pointer to Player
        self.player = event_handler.player

        # channel set to the proper synth
        self.channel = self.event_handler.channels[self.current_channel_index[0]]

    # Command to play note in context with record and play,
    # Will start recording or playing when note is played if record or play is held
    def play_note(self, index):
        # Normal press
        if not self.player.recording and not self.player.playing:
            self.channel.key_down(index)
        # If play button is held
        elif self.player.recording:
            if self.keyboard.shift:
                self.record_and_play(overwrite=False)
            else:
                self.record_and_play(overwrite=True)
            self.channel.key_down(index)
        # If record button is held
        elif self.player.playing:
            self.play()
            self.channel.key_down(index)

    def release_note(self, index):
        self.channel.key_up(index)

    def switch_mode(self, mode):
        self.event_handler.switch_mode(mode)

    def record_and_play(self, overwrite=True):
        if not self.player.recording and not self.player.playing:
            # Record
            self.player.record(overwrite=overwrite)

            if self.player.get_playlist():
                # plays all channels
                self.player.play_all()

    def play(self):
        # if any channels are not recording or player play
        if not self.player.recording and not self.player.playing:
            if self.player.get_playlist():
                # plays all channels
                self.player.play_all()

    def stop(self):
        self.player.stop_all()

    def octave_shift(self, octaves):
        # shift octave if possible
        if self.channel.octave_shift(octaves):
            # Check if there are any on notes
            for i in range(24):
                if i in self.keyboard.on_keys:
                    # Release the key
                    self.channel.key_up(i - octaves * 12)
                    # Play new notes
                    self.channel.key_down(i)

    def increment_volume(self, change):
        self.channel.increment_volume(change)

    def increment_modulation(self, change):
        self.channel.increment_modulation(change)

    def increment_pitch(self, change):
        self.channel.increment_pitch(change)

    def increment_balance(self, change):
        self.channel.increment_balance(change)

    def increment_pan(self, change):
        self.channel.increment_pan(change)

    def change_sustain(self, sustain):
        self.channel.change_sustain(sustain)

    def switch_channel(self, channel_num):
        self.event_handler.switch_channel(channel_num)
        Synth.midi_stop(self.channel.port)


class SoundSelect(Mode):
    def __init__(self, event_handler):
        super().__init__('soundselect', event_handler)

        # map each key to a function dictionary
        self.key_mappings = self.map_index2function()

        # Get list of all instrument addresses avaliable
        self.instr_key_list = list(self.channel.instr_dict.keys())

        if self.current_channel_index[0] == 9:
            # Only keep the drums
            drum_list = []
            for i in self.instr_key_list:
                if i[0] == 120:
                    drum_list.append(i)

            self.instr_key_list = drum_list

        # Get index of current instrument address in instr_key_list
        self.curr_instr = self.instr_key_list.index(tuple(self.channel.instr))

    def increment_instr(self, change):
        self.curr_instr = (self.curr_instr + change) % len(self.instr_key_list)
        self.channel.change_synth(self.instr_key_list[self.curr_instr][0],
                                  self.instr_key_list[self.curr_instr][1])

    def change_instr(self, bank, program):
        self.channel.change_synth(bank, program)
        self.curr_instr = self.instr_key_list.index(tuple(self.channel.instr))

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
            "shift",  # LShift
            "octave_down",  # left arrow
            "octave_up",  # right arrow
            "record",  # RShift
            "stop",  # Delete
            "play",  # Enter
            "channel_up",  # Up arrow
            "channel_down",  # Down arrow
            "select"  # Space bar
        ]

        return key_list

    def key_down(self, index):
        # if shift is pressed
        if self.keyboard.shift:

            # if playing piano keys
            if index < 24:
                self.play_note(index)

            # Switch modes
            elif self.key_mappings[index] == 'octave_up':
                self.switch_mode('test')

            # Switch modes
            elif self.key_mappings[index] == 'octave_down':
                self.switch_mode('freeplay')

            # Switch up an instrument
            elif self.key_mappings[index] == 'channel_up':
                self.increment_instr(1)

            # Switch down an instrument
            elif self.key_mappings[index] == 'channel_down':
                self.increment_instr(-1)

        # if playing piano keys
        elif index < 24:
            # if the record button or play button is held
            self.play_note(index)

        elif self.key_mappings[index] == 'octave_up':
            self.octave_shift(1)

        elif self.key_mappings[index] == 'octave_down':
            self.octave_shift(-1)

        # Switch up a channel
        elif self.key_mappings[index] == 'channel_up':
            self.switch_channel(self.current_channel_index[0] + 1)

        # Switch down a channel
        elif self.key_mappings[index] == 'channel_down':
            self.switch_channel(self.current_channel_index[0] - 1)

    def key_up(self, index):
        # if shift is pressed
        if self.keyboard.shift:
            # if playing piano keys
            if index < 24:
                self.release_note(index)

            # Recording without overwriting channel
            # elif self.key_mappings[index] == 'record':
            #     self.record(overwrite=False)

        elif index < 24:
            self.release_note(index)

        # Recording with overwriting channel
        elif self.key_mappings[index] == 'record':
            self.record_and_play(overwrite=True)
            self.switch_mode('freeplay')

        elif self.key_mappings[index] == 'play':
            self.play()

        elif self.key_mappings[index] == 'stop':
            self.stop()

    def use_knob(self, index, knob_num):
        print(index, knob_num)


class Freeplay(Mode):
    def __init__(self, event_handler):
        super().__init__('freeplay', event_handler)

        # map each key to a function dictionary
        self.key_mappings = self.map_index2function()

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
            "shift",  # LShift
            "octave_down",  # left arrow
            "octave_up",  # right arrow
            "record",  # RShift
            "stop",  # Delete
            "play",  # Enter
            "channel_up",  # Up arrow
            "channel_down",  # Down arrow
            "select"  # spacebar
        ]

        return key_list

    def key_down(self, index):
        # if shift is pressed
        if self.keyboard.shift:

            # if playing piano keys
            if index < 24:
                self.play_note(index)

            # Switch modes
            elif self.key_mappings[index] == 'octave_up':
                self.switch_mode('soundselect')

        # if playing piano keys
        elif index < 24:
            self.play_note(index)

        elif self.key_mappings[index] == 'octave_up':
            self.octave_shift(1)

        elif self.key_mappings[index] == 'octave_down':
            self.octave_shift(-1)

        # Switch up a channel
        elif self.key_mappings[index] == 'channel_up':
            self.switch_channel(self.current_channel_index[0] + 1)

        # Switch down a channel
        elif self.key_mappings[index] == 'channel_down':
            self.switch_channel(self.current_channel_index[0] - 1)

    def key_up(self, index):
        # if shift is pressed
        if self.keyboard.shift:
            # if playing piano keys
            if index < 24:
                self.release_note(index)

            elif self.key_mappings[index] == 'record':
                self.record_and_play(overwrite=False)

        elif index < 24:
            self.release_note(index)

        # record function
        elif self.key_mappings[index] == 'record':
            self.record_and_play(overwrite=True)

        elif self.key_mappings[index] == 'play':
            self.play()

        elif self.key_mappings[index] == 'stop':
            self.stop()

    def use_knob(self, index, knob_num):
        if knob_num == 0:
            pass


class Test(Mode):
    def __init__(self, event_handler):
        super().__init__('test', event_handler)

        # map each key to a function dictionary
        self.key_mappings = self.map_index2function()

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
            "shift",  # LShift
            "left",  # left arrow
            "right",  # right arrow
            "record",  # RShift
            "stop",  # Delete
            "play",  # Enter
            "up",  # Up arrow
            "down",  # Down arrow
            "spacebar",  # Spacebar
            "knob_1_up",  # KP 7
            "knob_1_down",  # KP 4
            "knob_2_up",  # KP 8
            "knob_2_down",  # KP 5
            "knob_3_up",  # KP 9
            "knob_3_down",  # KP 6
            "knob_4_up",  # KP -
            "knob_4_down",  # KP +
        ]

        return key_list

    def key_down(self, index):
        if self.keyboard.shift:
            if self.key_mappings[index] == 'octave_down':
                self.switch_mode('soundselect')

        # if playing piano keys
        elif index < 24:
            self.play_note(index)

        elif self.key_mappings[index] == 'octave_up':
            self.octave_shift(1)

        elif self.key_mappings[index] == 'octave_down':
            self.octave_shift(-1)

        # TODO: Trying knob up and knob down functions delete when actual knobs are connected
        elif self.key_mappings[index] == 'knob_1_up':
            self.use_knob(5, 0)

        elif self.key_mappings[index] == 'knob_1_down':
            self.use_knob(-5, 0)

        elif self.key_mappings[index] == 'knob_2_up':
            self.use_knob(5, 1)

        elif self.key_mappings[index] == 'knob_2_down':
            self.use_knob(-5, 1)

        elif self.key_mappings[index] == 'knob_3_up':
            self.use_knob(200, 2)

        elif self.key_mappings[index] == 'knob_3_down':
            self.use_knob(-200, 2)

        elif self.key_mappings[index] == 'knob_4_up':
            self.use_knob(5, 3)

        elif self.key_mappings[index] == 'knob_4_down':
            self.use_knob(-5, 3)

        elif self.key_mappings[index] == 'stop':
            self.change_sustain(True)

    def key_up(self, index):
        if index < 24:
            self.release_note(index)

        elif self.key_mappings[index] == 'stop':
            self.change_sustain(False)

    def use_knob(self, change, knob_num):
        if knob_num == 0:
            self.increment_volume(change)
        elif knob_num == 1:
            self.increment_modulation(change)
        elif knob_num == 2:
            self.increment_pitch(change)
        elif knob_num == 3:
            self.increment_pan(change)
