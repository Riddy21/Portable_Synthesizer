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

        # Locks for locking sustain and sustenuto
        self.sustain_lock = False
        self.sustenuto_lock = False

    # Command to play note in context with record and play,
    # Will start recording or playing when note is played if record or play is held
    def play_note(self, index):
        # Normal press
        if not self.keyboard.record and not self.keyboard.play:
            self.channel.key_down(index)
        # If record button is held
        elif self.keyboard.record:
            if self.keyboard.shift:
                self.record_and_play(overwrite=False)
            else:
                self.record_and_play(overwrite=True)
            self.channel.key_down(index)
        # If the play button is held
        elif self.keyboard.play:
            self.play()
            self.channel.key_down(index)

    def release_note(self, index):
        self.channel.key_up(index)

    def switch_mode(self, mode):
        self.event_handler.switch_mode(mode, self.current_channel_index[0])

    def switch_channel(self, channel_num):
        Synth.midi_stop(self.channel.port)
        if not self.sustain_lock and self.channel.sustain == 64:
            self.change_sustain(False)
        if not self.sustenuto_lock and self.channel.sustenuto == 64:
            self.change_sustenuto(False, self.channel.channel_ind)
        self.event_handler.switch_channel(channel_num)

    def increment_channel(self, change):
        channel_num = self.current_channel_index[0] + change
        self.switch_channel(channel_num)

    def update(self):
        self.channel = self.event_handler.channels[self.current_channel_index[0]]

    def increment_time(self, change):
        self.player.increment_start_time(change)

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

    def toggle_sustain(self):
        self.channel.toggle_sustain()

    def change_sustenuto(self, sustenuto):
        self.channel.change_sustenuto(sustenuto)

    def toggle_sustenuto(self):
        self.channel.toggle_sustenuto()

    def increment_reverb(self, change):
        self.channel.increment_reverb(change)

    def increment_chorus(self, change):
        self.channel.increment_chorus(change)

    def increment_velocity(self, change):
        self.channel.increment_velocity(change)


    # ----- Interface Methods ------
    def key_down(self, key):
        # if playing piano keys
        if type(key) is int:
            self.play_note(key)

        # Octave change
        if key == 'left_arrow':
            self.octave_shift(-1)
        elif key == 'right_arrow':
            self.octave_shift(1)

        # Sustenuto
        elif key == 'sustenuto':
            # Cannot lock when playing
            if self.keyboard.shift and not self.player.playing:
                self.toggle_sustenuto()
                self.sustenuto_lock = not self.sustenuto_lock
            else:
                self.change_sustenuto(True)

        # Sustain
        elif key == 'sustain':
            # Cannot lock when playing
            if self.keyboard.shift and not self.player.playing:
                self.toggle_sustain()
                self.sustain_lock = not self.sustain_lock
            else:
                self.change_sustain(True)

    def key_up(self, key):
        # if playing piano keys
        if type(key) is int:
            self.release_note(key)

        # Sustenuto
        elif key == 'sustenuto':
            if not self.sustenuto_lock:
                self.change_sustenuto(False)

        # Sustain
        elif key == 'sustain':
            if not self.sustain_lock:
                self.change_sustain(False)
    def use_knob(self, change, knob_num):
        pass

class Record(Mode):
    def __init__(self, event_handler):
        super().__init__('record', event_handler)

    def key_down(self, key):
        super().key_down(key)
        # TODO: Knobs that will be replaced with knob functions
        if key == 'knob_1_up':
            self.use_knob(0.2, 0)
        elif key == 'knob_1_down':
            self.use_knob(-0.2, 0)
        elif key == 'knob_4_up':
            self.use_knob(1, 3)
        elif key == 'knob_4_down':
            self.use_knob(-1, 3)

    def key_up(self, key):
        super().key_up(key)

        # Recording with overwriting channel
        if key == 'record':
            if self.keyboard.shift:
                self.record_and_play(overwrite=False)
            else:
                self.record_and_play(overwrite=True)

        elif key == 'play':
            self.play()

        elif key == 'stop':
            self.stop()

    def use_knob(self, change, knob_num):
        if knob_num == 0:
            self.increment_time(change)
        elif knob_num == 3:
            self.increment_channel(change)


class Test(Mode):
    def __init__(self, event_handler):
        super().__init__('test', event_handler)

    def key_down(self, key):
        if self.keyboard.shift:
            if key == 'right_arrow':
                self.switch_mode('record')

        # if playing piano keys
        elif type(key) is int:
            self.play_note(key)

        elif key == 'right_arrow':
            self.octave_shift(1)

        elif key == 'left_arrow':
            self.octave_shift(-1)

        # TODO: Trying knob up and knob down functions delete when actual knobs are connected
        elif key == 'knob_1_up':
            self.use_knob(5, 0)

        elif key == 'knob_1_down':
            self.use_knob(-5, 0)

        elif key == 'knob_2_up':
            self.use_knob(5, 1)

        elif key == 'knob_2_down':
            self.use_knob(-5, 1)

        elif key == 'knob_3_up':
            self.use_knob(5, 2)

        elif key == 'knob_3_down':
            self.use_knob(-5, 2)

        elif key == 'knob_4_up':
            self.use_knob(5, 3)

        elif key == 'knob_4_down':
            self.use_knob(-5, 3)

        elif key == 'stop':
            self.change_sustenuto(True)

    def key_up(self, key):
        if type(key) is int:
            self.release_note(key)
        elif key == 'stop':
            self.change_sustenuto(False)

    def use_knob(self, change, knob_num):
        if knob_num == 0:
            self.increment_pan(change)
        elif knob_num == 1:
            self.increment_volume(change)
        elif knob_num == 2:
            self.increment_reverb(change)
        elif knob_num == 3:
            self.increment_chorus(change)

class SoundSelect(Mode):
    def __init__(self, event_handler):
        super().__init__('soundselect', event_handler)

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

   # override function for update to update instruments too 
    def update(self):
        self.channel = self.event_handler.channels[self.current_channel_index[0]]
        self.curr_instr = self.instr_key_list.index(tuple(self.channel.instr))

    def key_down(self, key):
        # if shift is pressed
        if self.keyboard.shift:

            # if playing piano keys
            if type(key) is int:
                self.play_note(key)

            # Switch modes
            elif key == 'right_arrow':
                self.switch_mode('test')

            # Switch modes
            elif key == 'left_arrow':
                self.switch_mode('freeplay')

            # Switch up an instrument
            elif key == 'knob_1_up':
                self.increment_instr(1)

            # Switch down an instrument
            elif key == 'knob_1_down':
                self.increment_instr(-1)

        # if playing piano keys
        elif type(key) is int:
            # if the record button or play button is held
            self.play_note(key)

        elif key == 'right_arrow':
            self.octave_shift(1)

        elif key == 'left_arrow':
            self.octave_shift(-1)

        # Switch up a channel
        elif key == 'knob_1_up':
            self.switch_channel(self.current_channel_index[0] + 1)

        # Switch down a channel
        elif key == 'knob_1_down':
            self.switch_channel(self.current_channel_index[0] - 1)

    def key_up(self, key):
        # if shift is pressed
        if self.keyboard.shift:
            # if playing piano keys
            if type(key) is int:
                self.release_note(key)

            # Recording without overwriting channel
            # elif self.key_mappings[key] == 'record':
            #     self.record(overwrite=False)

        elif type(key) is int:
            self.release_note(key)

        # Recording with overwriting channel
        elif key == 'record':
            self.record_and_play(overwrite=True)
            self.switch_mode('freeplay')

        elif key == 'play':
            self.play()

        elif key == 'stop':
            self.stop()

    def use_knob(self, index, knob_num):
        print(index, knob_num)


class Freeplay(Mode):
    def __init__(self, event_handler):
        super().__init__('freeplay', event_handler)

    def key_down(self, key):
        # if shift is pressed
        if self.keyboard.shift:

            # if playing piano keys
            if type(key) is int:
                self.play_note(key)

            # Switch modes
            elif key == 'right_arrow':
                self.switch_mode('soundselect')

        # if playing piano keys
        elif type(key) is int:
            self.play_note(key)

        elif key == 'right_arrow':
            self.octave_shift(1)

        elif key == 'left_arrow':
            self.octave_shift(-1)

        # Switch up a channel
        elif key == 'knob_1_up':
            self.switch_channel(self.current_channel_index[0] + 1)

        # Switch down a channel
        elif key == 'knob_1_down':
            self.switch_channel(self.current_channel_index[0] - 1)

    def key_up(self, key):
        # if shift is pressed
        if self.keyboard.shift:
            # if playing piano keys
            if type(key) is int:
                self.release_note(key)

            elif key == 'record':
                self.record_and_play(overwrite=False)

        elif type(key) is int:
            self.release_note(key)

        # record function
        elif key == 'record':
            self.record_and_play(overwrite=True)

        elif key == 'play':
            self.play()

        elif key == 'stop':
            self.stop()

    def use_knob(self, index, knob_num):
        if knob_num == 0:
            pass
