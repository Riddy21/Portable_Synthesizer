from synth import Synth
import time
import pygame
from threading_decorator import run_in_thread


# Class for connecting synths with the keyboard or handling it with other players
class PlaybackHandler(object):
    def __init__(self, keyboard):
        # initialize channels and the keyboard
        self.channels = []
        self.keyboard = keyboard

        # Set the playback hanlder on the keyboard to be this one
        self.keyboard.set_handler(self)

        # set the player/recorder and pass channels
        self.player = Player(self.channels)

        # Set the current mode to none
        self.current_mode = None
        self.current_channel_index = None

    # Add a new channel and declare its playing mode
    def add_channel(self, mode, port, instr=0, reverb=0.3, gain=270):
        # Find the channel number
        channel_length = len(self.channels)

        # Make the synth and add it to channels
        synth = Synth(mode=mode, channel=channel_length, recorder=self.player, port=port, instr=instr, reverb=reverb,
                      gain=gain)
        self.channels.append(synth)

        self.current_channel_index = channel_length

        # set the current playing mode and send the synth to it
        self.switch_mode('freeplay')

    # Switch the mode of the current channel
    def switch_mode(self, mode):
        synth = self.channels[self.current_channel_index]
        if mode == 'freeplay':
            self.current_mode = Freeplay(synth, keyboard=self.keyboard, playback_handler=self)
        elif mode == 'test':
            self.current_mode = Test(synth, keyboard=self.keyboard, playback_handler=self)

    # Switch the current channel
    def switch_channel(self, channel_ind):
        # change the channel
        self.current_channel_index = channel_ind

        # change the mode
        self.switch_mode(self.channels[channel_ind].mode)

    # ------------------
    # Interface for passing to current mode
    # ------------------
    def key_down(self, index):
        self.current_mode.key_down(index)

    def key_up(self, index):
        self.current_mode.key_up(index)

    def use_knob(self, index, knob_num):
        if knob_num == 0:
            self.current_mode.use_knob(index, knob_num)


# player for recording and playing certain channels
class Player(object):
    def __init__(self, channels):
        self.channels = channels
        self.recording = False
        self.playing = False

        self.recordlist = []
        self.playlist = []

    def record_event(self, time, channel, event):
        # if is recording
        if self.recording:
            print(time - self.recording, event[1])
            # add event to playlist
            self.recordlist.append([time - self.recording, channel, event])

    # plays all the channels at the same time
    @run_in_thread
    def play_all(self):
        self.playing = True
        # sort the list by time
        start = time.time()
        self.playlist = sorted(self.playlist, key=lambda l: l[0])
        end = time.time()
        # print(self.playlist)

        # Tracks starting time
        start_time = time.time()

        for event in self.playlist:
            # Get the proper channel to play
            channel = self.channels[event[1]]

            # If was stopped
            if self.playing == False:
                # turn off all notes
                channel.midi_stop()

                break

            note_time = event[0]

            # wait until time to play note
            while time.time() - start_time <= note_time:
                pygame.time.delay(1)

            # play the event
            if event[2][0] == 'note_on':
                channel.midi_note_on(event[2][1], background_mode=True)
            elif event[2][0] == 'note_off':
                channel.midi_note_off(event[2][1], background_mode=True)
            if event[2][0] == 'program_change':
                channel.midi_change_synth(event[2][1], background_mode=True)

        print('end')
        self.playing = False

    # record all the channels at the same time
    def record(self):
        self.recordlist = []
        self.recording = time.time()

    # Stops all playing and stops recording
    def stop_all(self):
        # move record list to play list
        if self.recording:
            self.playlist += self.recordlist
        self.recording = False
        self.playing = False

    def pause(self, channel_ind):
        pass


# ------------------
# Mode controllers
# ------------------

# Parent object for all modes
class Mode(object):
    def __init__(self, name, synth, keyboard, playback_handler):
        self.name = name

        # channel set to the proper synth
        self.channel = synth

        # Keybaord pointer
        self.keyboard = keyboard

        # Playback handler pointer for switching modes
        self.playback_handler = playback_handler

        # Get pointer to Player
        self.player = playback_handler.player


class Freeplay(Mode):
    def __init__(self, synth, keyboard, playback_handler):
        super().__init__('freeplay', synth, keyboard, playback_handler)

        # map each key to a function dictionary
        self.key_mappings = self.map_index2function()

        self.channel.change_synth(2)

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
        ]

        return key_list

    def key_down(self, index):
        # if shift is pressed
        if self.keyboard.shift:
            # if playing piano keys
            if index < 24:
                pass
            elif self.key_mappings[index] == 'octave_up':
                self.playback_handler.switch_mode('test')
        # if playing piano keys
        elif index < 24:
            self.channel.key_down(index)
        elif self.key_mappings[index] == 'octave_up':
            # shift octave if possible
            if self.channel.octave_shift(1):
                # Check if there are any on notes
                for i in range(24):
                    if i in self.keyboard.on_keys:
                        # Release the key
                        self.channel.key_up(i - 12)
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


class Test(Mode):
    def __init__(self, synth, keyboard, playback_handler):
        super().__init__('test', synth, keyboard, playback_handler)

        # map each key to a function dictionary
        self.key_mappings = self.map_index2function()

        self.channel.change_synth(0)

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
        ]

        return key_list

    def key_down(self, index):
        # if shift is pressed
        if self.keyboard.shift:
            # if playing piano keys
            if index < 24:
                pass
            elif self.key_mappings[index] == 'octave_down':
                self.playback_handler.switch_mode('freeplay')

        # if playing piano keys
        elif index < 24:
            # if the record button is held
            if 27 in self.keyboard.on_keys:
                self.key_up(27)

            self.channel.key_down(index)

        # Play the recording list
        elif self.key_mappings[index] == 'play':
            # if any channels are not recording or player play
            if not self.player.recording and not self.player.playing:
                self.player.play_all()

    def key_up(self, index):
        if index < 24:
            self.channel.key_up(index)
        # record function
        elif self.key_mappings[index] == 'record':
            if not self.player.recording and not self.player.playing:
                self.player.record()

                # plays all channels
                self.player.play_all()

        elif self.key_mappings[index] == 'stop':
            self.player.stop_all()

    def use_knob(self, index, knob_num):
        if knob_num == 0:
            self.channel.change_synth(index)
