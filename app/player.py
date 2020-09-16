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
        # for gui tracking what time it currently is
        self.current_time = 0

        self.recording = False
        self.playing = False

        self.recordlist = []
        self.playlist = set()

    def record_event(self, msg, time, setup=False):
        # if is recording
        if self.recording:
            # Get the time in reference to the starting of the recording
            timestamp = time - self.recording + self.start_time

            if setup:
                event = (timestamp, tuple(msg), 'setup')
            else:
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
            note_time = event[0]

            # wait until time to play note
            while time.time() - start_time <= note_time:
                # If was stopped
                if not self.playing:
                    # turn off all notes
                    Synth.midi_stop(self.port)
                    self.current_time = self.start_time
                    return
                self.current_time = time.time() - start_time + self.start_time
                pygame.time.delay(1)
            Synth.send_msg(self.channels, event[1])
            #print(event)

        self.playing = False
        self.current_time = self.start_time

    # record all the channels at the same time
    def record(self, overwrite):
        # Stop all channels
        Synth.midi_stop(self.channels[0].port)

        self.recording = time.time()

        # Delete whatever was ther before if overwriting
        if overwrite:
            self.delete_channel(self.current_channel_index[0], self.start_time, 'right')

        # Add the initial information such as channel synth, gain, reverb, volume to the
        # beginning of the record list of the channel you are on right now of only the channel youre on right now
        # Record setup for all channels
        for channel in self.channels:
            if channel:
                if self.start_time == 0:
                    channel.record_setup(self.recording)
                else:
                    self.find_record_track_setup(self.start_time)

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

        self.current_time = self.start_time

    # Find the setup right before in the recording
    def find_record_track_setup(self, start_time):
        # Make an empty list of 16 dictionaries to store all information about setup and time
        # Initialize time as -1 so it gets overridden
        setup = []
        for channel in range(16):
            setup.append({
                'program': (None, -1),
                'bank': (None, -1),
                'volume': (None, -1),
                'modulation': (None, -1),
                'balance': (None, -1),
                'pan': (None, -1),
                'sustain': (None, -1),
                'sustenuto': (None, -1),
                'reverb': (None, -1),
                'chorus': (None, -1),
                'pitch': (None, -1)
                })

        # Loop through all events
        for event in self.playlist:

            # Decode message
            msg = Synth.bytes2msg(event[1])
            timestamp = event[0]


            # If the event was before the start time
            if timestamp < start_time:
                # Save latest program changes and control changes to setup the sound environment
                if msg.type == 'program_change':
                    prev_time = setup[msg.channel]['program'][1]
                    if prev_time < timestamp:
                        setup[msg.channel]['program'] = (msg, timestamp)
                elif msg.type == 'control_change':
                    if msg.control == 0:
                        prev_time = setup[msg.channel]['bank'][1]
                        if prev_time < timestamp:
                            setup[msg.channel]['bank'] = (msg, timestamp)
                    elif msg.control == 7:
                        prev_time = setup[msg.channel]['volume'][1]
                        if prev_time < timestamp:
                            setup[msg.channel]['volume'] = (msg, timestamp)
                    elif msg.control == 1:
                        prev_time = setup[msg.channel]['modulation'][1]
                        if prev_time < timestamp:
                            setup[msg.channel]['modulation'] = (msg, timestamp)
                    elif msg.control == 8:
                        prev_time = setup[msg.channel]['balance'][1]
                        if prev_time < timestamp:
                            setup[msg.channel]['balance'] = (msg, timestamp)
                    elif msg.control == 10:
                        prev_time = setup[msg.channel]['pan'][1]
                        if prev_time < timestamp:
                            setup[msg.channel]['pan'] = (msg, timestamp)
                    elif msg.control == 64:
                        prev_time = setup[msg.channel]['sustain'][1]
                        if prev_time < timestamp:
                            setup[msg.channel]['sustain'] = (msg, timestamp)
                    elif msg.control == 66:
                        prev_time = setup[msg.channel]['sustenuto'][1]
                        if prev_time < timestamp:
                            setup[msg.channel]['sustenuto'] = (msg, timestamp)
                    elif msg.control == 91:
                        prev_time = setup[msg.channel]['reverb'][1]
                        if prev_time < timestamp:
                            setup[msg.channel]['reverb'] = (msg, timestamp)
                    elif msg.control == 93:
                        prev_time = setup[msg.channel]['chorus'][1]
                        if prev_time < timestamp:
                            setup[msg.channel]['chorus'] = (msg, timestamp)
                elif msg.type == 'pitchwheel':
                    prev_time = setup[msg.channel]['pitch'][1]
                    if prev_time < timestamp:
                        setup[msg.channel]['pitch'] = (msg, timestamp)

        # add all of setup msgs to the list with time at 0
        for channel in setup:
            for setting in channel.values():

                if not setting[0]:
                    continue
                # must change program before changing bank

                # If program change, set the event timestamp  so it happens after control change
                if setting[0].type == 'program_change':
                    self.record_event(time=self.recording+0.00001, msg = setting[0].bytes(), setup=True)
                else:
                    self.record_event(time=self.recording, msg = setting[0].bytes(), setup=True)



    # cleans up and sorts the playlist
    def make_event_list(self):
        event_list = []

        # Make an empty list of 16 dictionaries to store all information about setup and time
        # Initialize time as -1 so it gets overridden
        setup = []
        for channel in range(16):
            setup.append({
                'program': (None, -1),
                'bank': (None, -1),
                'volume': (None, -1),
                'modulation': (None, -1),
                'balance': (None, -1),
                'pan': (None, -1),
                'sustain': (None, -1),
                'sustenuto': (None, -1),
                'reverb': (None, -1),
                'chorus': (None, -1),
                'pitch': (None, -1)
                })

        # Loop through all events
        for event in self.playlist:

            # Decode message
            msg = Synth.bytes2msg(event[1])
            timestamp = event[0]


            # If the event was before the start time
            if timestamp < self.start_time:
                # Save latest program changes and control changes to setup the sound environment
                if msg.type == 'program_change':
                    prev_time = setup[msg.channel]['program'][1]
                    if prev_time < timestamp:
                        setup[msg.channel]['program'] = (msg, timestamp)
                elif msg.type == 'control_change':
                    if msg.control == 0:
                        prev_time = setup[msg.channel]['bank'][1]
                        if prev_time < timestamp:
                            setup[msg.channel]['bank'] = (msg, timestamp)
                    elif msg.control == 7:
                        prev_time = setup[msg.channel]['volume'][1]
                        if prev_time < timestamp:
                            setup[msg.channel]['volume'] = (msg, timestamp)
                    elif msg.control == 1:
                        prev_time = setup[msg.channel]['modulation'][1]
                        if prev_time < timestamp:
                            setup[msg.channel]['modulation'] = (msg, timestamp)
                    elif msg.control == 8:
                        prev_time = setup[msg.channel]['balance'][1]
                        if prev_time < timestamp:
                            setup[msg.channel]['balance'] = (msg, timestamp)
                    elif msg.control == 10:
                        prev_time = setup[msg.channel]['pan'][1]
                        if prev_time < timestamp:
                            setup[msg.channel]['pan'] = (msg, timestamp)
                    elif msg.control == 64:
                        prev_time = setup[msg.channel]['sustain'][1]
                        if prev_time < timestamp:
                            setup[msg.channel]['sustain'] = (msg, timestamp)
                    elif msg.control == 66:
                        prev_time = setup[msg.channel]['sustenuto'][1]
                        if prev_time < timestamp:
                            setup[msg.channel]['sustenuto'] = (msg, timestamp)
                    elif msg.control == 91:
                        prev_time = setup[msg.channel]['reverb'][1]
                        if prev_time < timestamp:
                            setup[msg.channel]['reverb'] = (msg, timestamp)
                    elif msg.control == 93:
                        prev_time = setup[msg.channel]['chorus'][1]
                        if prev_time < timestamp:
                            setup[msg.channel]['chorus'] = (msg, timestamp)
                elif msg.type == 'pitchwheel':
                    prev_time = setup[msg.channel]['pitch'][1]
                    if prev_time < timestamp:
                        setup[msg.channel]['pitch'] = (msg, timestamp)

                # Dont add to curated list
            else:
                if len(event) == 3:
                    continue
                msg = Synth.bytes2msg(event[1])
                # shift the timing to align with the start_time
                event_list.append((event[0] - self.start_time, msg))

        # add all of setup msgs to the list with time at 0
        for channel in setup:
            for setting in channel.values():

                if not setting[0]:
                    continue
                # must change program before changing bank

                # If program change, set the event timestamp  so it happens after control change
                if setting[0].type == 'program_change':
                    event_list.append((0.00001, setting[0]))
                else:
                    event_list.append((0.0, setting[0]))

        return sorted(event_list, key=lambda l: l[0])

    # Save playlist as a file
    def save_to_file(self):
        timestr = time.strftime("Data/Date: %m_%d_%Y Time:%H_%M_%S")
        file = open(timestr + '.txt', 'w')

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
        except ValueError:
            pass

        # Save back into set format
        for elem in playlist_data:
            time = float(elem[0])
            tmplist = []
            for i in range(1, len(elem)):
                tmplist.append(int(elem[i]))
            new_playlist.add((time, tuple(tmplist)))

        self.playlist = new_playlist

    # sets the start time
    def set_start_time(self, start_time):
        if not self.playing and not self.recording and start_time >= 0:
            self.start_time = start_time
            self.current_time = self.start_time

    def increment_start_time(self, increment):
        start_buff = self.start_time + increment
        if not self.playing and not self.recording and start_buff >= 0:
            self.start_time = round(start_buff,4)
            self.current_time = self.start_time

    # Deletes everything in a channel from a time onwards
    def delete_channel(self, channel_ind, time, direction):
        # start = time.time()
        remove_list = []
        # find
        for event in self.playlist:
            msg = Synth.bytes2msg(event[1])
            if direction == 'right':
                if msg.channel == channel_ind and event[0] >= round(time, 4):
                    remove_list.append(event)
            elif direction == 'left':
                if msg.channel == channel_ind and event[0] <= round(time, 4):
                    remove_list.append(event)


        # Remove
        for event in remove_list:
            self.playlist.remove(event)

        # end = time.time()

    # TODO: Make delete effects function
    def delete_effects(self, channel_ind, time, direction):
        pass


    def get_playlist(self):
        return self.playlist
