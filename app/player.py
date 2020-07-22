import time
import pygame
from threading_decorator import run_in_thread
from synth import Synth


# player for recording and playing certain channels
class Player(object):
    def __init__(self, channels, playback_handler):
        self.channels = channels
        self.playback_handler = playback_handler
        self.recording = False
        self.playing = False

        self.recordlist = []
        self.playlist = []

    def record_event(self, time, channel, event):
        # if is recording
        if self.recording:
            # add event to playlist
            self.recordlist.append([time - self.recording, channel, event])

    # plays all the channels at the same time
    @run_in_thread
    def play_all(self):
        self.playing = True
        # sort the list by time
        self.playlist = sorted(self.playlist, key=lambda l: l[0])

        # Tracks starting time
        start_time = time.time()

        for event in self.playlist:
            # Get the proper channel to play
            channel = self.channels[event[1]]

            # If was stopped
            if not self.playing:
                # turn off all notes
                Synth.midi_stop(channel.port)

                break

            note_time = event[0]

            # wait until time to play note
            while time.time() - start_time <= note_time:
                pygame.time.delay(1)

            # play the event directly to avoid keyboard interface
            if event[2][0] == 'note_on':
                channel.midi_note_on(event[2][1], background_mode=True)
            elif event[2][0] == 'note_off':
                channel.midi_note_off(event[2][1], background_mode=True)
            if event[2][0] == 'program_change':
                channel.midi_change_synth(event[2][1], background_mode=True)

        self.playing = False

    # record all the channels at the same time
    def record(self):
        # Stop all channels
        Synth.midi_stop(self.channels[0].port)

        # Add the initial information such as channel synth, gain, reverb, volume to the
        # beginning of the record list of the channel you are on right now of only the channel youre on right now
        current_channel_index = self.playback_handler.current_channel_index
        current_channel = self.channels[current_channel_index]
        self.recordlist.append([0, current_channel_index, ['program_change', current_channel.instr]])

        # Delete everything on that channel previously
        self.delete_channel(current_channel_index)

        self.recording = time.time()

    # Stops all playing and stops recording
    def stop_all(self):
        # turn off all notes
        Synth.midi_stop(self.channels[0].port)
        # move record list to play list and clear record list
        if self.recording:
            self.playlist += self.recordlist
            self.recordlist = []
        self.recording = False
        self.playing = False

    def pause(self, channel_ind):
        pass

    # Deletes everything in a channel
    def delete_channel(self, channel_ind):
        start = time.time()
        remove_list = []
        # find
        for event in self.playlist:
            if event[1] == channel_ind:
                remove_list.append(event)

        # Remove
        for event in remove_list:
            self.playlist.remove(event)

        end = time.time()

