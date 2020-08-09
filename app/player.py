import time
import pygame
import os
from threading_decorator import run_in_thread
from synth import Synth


# player for recording and playing certain channels
class Player(object):

    def __init__(self, event_handler):
        # Variables from event handler
        self.channels = event_handler.channels
        self.port = event_handler.port
        self.current_channel_index = event_handler.current_channel_index  # Is a primitive so references as address

        # Time at which playing and recording starts at
        self.start_time = 0

        self.recording = False
        self.playing = False

        self.recordlist = []
        self.playlist = set()

    def record_event(self, msg, time):
        # if is recording
        if self.recording:
            # Get the time in reference to the starting of the recording
            timestamp = time - self.recording + self.start_time

            event = (timestamp, tuple(msg))

            # add event to playlist
            self.recordlist.append(event)

    # plays all the channels at the same time
    @run_in_thread
    def play_all(self):
        self.playing = True

        # reorganize and sort playlist
        event_list = self.make_event_list()

        # Tracks starting time
        start_time = time.time()

        for event in event_list:
            # If was stopped
            if not self.playing:
                # turn off all notes
                Synth.midi_stop(self.port)
                break

            note_time = event[0]

            # wait until time to play note
            while time.time() - start_time <= note_time:
                pygame.time.delay(1)

            Synth.send_msg(self.channels, event[1])

        self.playing = False

    # record all the channels at the same time
    def record(self, overwrite):
        # Stop all channels
        Synth.midi_stop(self.channels[0].port)

        self.recording = time.time()

        # Add the initial information such as channel synth, gain, reverb, volume to the
        # beginning of the record list of the channel you are on right now of only the channel youre on right now
        current_channel = self.channels[self.current_channel_index[0]]
        current_channel.record_setup()

        if overwrite:
            self.delete_channel(self.current_channel_index[0])

    # Stops all playing and stops recording
    def stop_all(self):
        # turn off all notes
        Synth.midi_stop(self.channels[0].port)
        # move record list to play list and clear record list
        if self.recording:
            self.playlist = self.playlist.union(self.recordlist)
            self.recordlist = []
        self.recording = False
        self.playing = False

    # cleans up and sorts the playlist
    def make_event_list(self):
        event_list = []

        # Make an empty list of 16 dictionaries to store all information about setup
        setup = []
        for channel in range(16):
            setup.append(dict())

        # Loop through all events
        for event in self.playlist:

            # Decode message
            msg = Synth.bytes2msg(event[1])
            timestamp = event[0]

            # If the event was before the start time
            if timestamp < self.start_time:
                # Save latest program changes and control changes to setup the sound environment
                if msg.type == 'program_change':
                    setup[msg.channel]['program'] = msg
                elif msg.type == 'control_change':
                    if msg.control == 0:
                        setup[msg.channel]['bank'] = msg

                # Dont add to curated list
            else:
                msg = Synth.bytes2msg(event[1])
                # shift the timing to align with the start_time
                event_list.append((event[0] - self.start_time, msg))

        # add all of setup msgs to the list with time at 0
        for channel in setup:
            for setting in channel.values():
                # must change program before changing bank

                # If program change, set the event timestamp as 0.0001
                if setting.type == 'program_change':
                    event_list.append((0.0001, setting))
                else:
                    event_list.append((0, setting))

        return sorted(event_list, key=lambda l: l[0])

    # Save playlist as a file
    def save_to_file(self):
        timestr = time.strftime("Data/Date: %m_%d_%Y Time:%H_%M_%S")
        file = open(timestr+'.txt', 'w')
        
        string = ""
        for event in self.playlist:
            string += str(event[0])
            for elem in event[1]:
                string += ' ' + str(elem)
            string += '\n'

        file.write(string)
        file.close()


    # Gets list of projects you are working on
    def get_projects(self):
        return os.listdir('Data/')

    # Load a playlist as an object
    def load_from_file(self, filename):
        # Get file
        filepath = os.path.join('Data', filename)
        file = open(filepath, 'r')

        # Parse playlist_data
        playlist_data = file.read()
        playlist_data = playlist_data.split('\n')

        # Make empty set
        new_playlist = set()

        # parse into 2D list
        for line_index in range(len(playlist_data)):
            playlist_data[line_index] = playlist_data[line_index].split(' ')
    
        # remove empty elements
        try:
            playlist_data.remove([''])
            print('removed!')
        except ValueError:
            pass

        # Save back into set format
        for elem in playlist_data:
            time = float(elem[0])
            tmplist = []
            for i in range(1,len(elem)):
                tmplist.append(int(elem[i]))
            new_playlist.add((time, tuple(tmplist)))
        
        self.playlist = new_playlist

    # sets the start time
    def set_start_time(self, start_time):
        if start_time >= 0:
            self.start_time = start_time

    # Deletes everything in a channel from a time onwards
    def delete_channel(self, channel_ind):
        # start = time.time()
        remove_list = []
        # find
        for event in self.playlist:
            msg = Synth.bytes2msg(event[1])
            if msg.channel == channel_ind and event[0] >= self.start_time:
                remove_list.append(event)

        # Remove
        for event in remove_list:
            self.playlist.remove(event)

        # end = time.time()

    def get_playlist(self):
        return self.playlist
