import time
import pygame
from threading_decorator import run_in_thread
from synth import Synth


# player for recording and playing certain channels
class Player(object):
    def __init__(self, event_handler):
        # Variables from event handler
        self.channels = event_handler.channels
        self.port = event_handler.port
        self.current_channel_index = event_handler.current_channel_index  # Is a primitive so references as address

        self.recording = False
        self.playing = False

        self.recordlist = []
        self.playlist = set()

    def record_event(self, time, msg):
        # if is recording
        if self.recording:
            # add event to playlist
            self.recordlist.append((time, msg))

    # plays all the channels at the same time
    @run_in_thread
    def play_all(self):
        self.playing = True

        # reorganize and sort playlist
        self.clean_up_playlist()

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
            if event[2][0] == 'synth_change':
                channel.midi_change_synth(bank=event[2][1], program=event[2][2], background_mode=True)

        self.playing = False

    # record all the channels at the same time
    def record(self, overwrite):
        # Stop all channels
        Synth.midi_stop(self.channels[0].port)

        # Add the initial information such as channel synth, gain, reverb, volume to the
        # beginning of the record list of the channel you are on right now of only the channel youre on right now
        current_channel = self.channels[self.current_channel_index[0]]
        current_channel.record_setup()

        if overwrite:
            self.delete_channel(self.current_channel_index[0])

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

    # cleans up and sorts the playlist
    def clean_up_playlist(self):
        # sort the list by time
        self.playlist = sorted(self.playlist, key=lambda l: l[0])

    # Deletes everything in a channel
    def delete_channel(self, channel_ind):
        # start = time.time()
        remove_list = []
        # find
        for event in self.playlist:
            if event[1] == channel_ind:
                remove_list.append(event)

        # Remove
        for event in remove_list:
            self.playlist.remove(event)

        # end = time.time()

    def get_playlist(self):
        return self.playlist

