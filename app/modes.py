# ------------------
# Mode controllers
# ------------------

# Parent object for all modes
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
        ]

        return key_list

    def key_down(self, index):
        # if shift is pressed
        if self.keyboard.shift:

            # if playing piano keys
            if index < 24:
                # if the record button is held
                if self.keyboard.is_on(27):
                    self.key_up(27)
                elif self.keyboard.is_on(29):
                    self.key_up(29)

                self.channel.key_down(index)

            # Switch modes
            elif self.key_mappings[index] == 'octave_up':
                self.event_handler.switch_mode('test')

            # Switch Synth
            elif self.key_mappings[index] == 'channel_up':
                self.channel.change_synth(self.channel.instr + 1)

            # Switch Synth
            elif self.key_mappings[index] == 'channel_down':
                self.channel.change_synth(self.channel.instr - 1)

        # if playing piano keys
        elif index < 24:
            # if the record button is held
            if self.keyboard.is_on(27):
                self.key_up(27)
            elif self.keyboard.is_on(29):
                self.key_up(29)

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

        # Switch up a channel
        elif self.key_mappings[index] == 'channel_up':
            self.event_handler.switch_channel(self.current_channel_index[0] + 1)

        # Switch down a channel
        elif self.key_mappings[index] == 'channel_down':
            self.event_handler.switch_channel(self.current_channel_index[0] - 1)


    def key_up(self, index):
        # if shift is pressed
        if self.keyboard.shift:
            # if playing piano keys
            if index < 24:
                self.channel.key_up(index)

            elif self.key_mappings[index] == 'record':
                if not self.player.recording and not self.player.playing:
                    # Record
                    self.player.record(overwrite=False)

                    # plays all channels
                    self.player.play_all()

        elif index < 24:
            self.channel.key_up(index)

        # record function
        elif self.key_mappings[index] == 'record':
            if not self.player.recording and not self.player.playing:
                self.player.record(overwrite=True)

                # plays all channels
                self.player.play_all()

                # Play the recording list
        elif self.key_mappings[index] == 'play':
            # if any channels are not recording or player play
            if not self.player.recording and not self.player.playing:
                self.player.play_all()

        elif self.key_mappings[index] == 'stop':
            self.player.stop_all()

    def use_knob(self, index, knob_num):
        if knob_num == 0:
            self.channel.change_synth(index)


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
            "octave_down",  # left arrow
            "octave_up",  # right arrow
            "record",  # RShift
            "stop",  # Delete
            "play",  # Enter
            "channel_up",  # Up arrow
            "channel_down"  # Down arrow
        ]

        return key_list

    def key_down(self, index):
        # if shift is pressed
        if self.keyboard.shift:

            # if playing piano keys
            if index < 24:
                pass

            # Switch modes
            elif self.key_mappings[index] == 'octave_down':
                self.event_handler.switch_mode('freeplay')

            # Switch Synth
            elif self.key_mappings[index] == 'channel_up':
                self.channel.change_synth(self.channel.instr + 1)

            # Switch Synth
            elif self.key_mappings[index] == 'channel_down':
                self.channel.change_synth(self.channel.instr - 1)
        # if playing piano keys
        elif index < 24:
            # if the record button is held
            if 27 in self.keyboard.on_keys:
                self.key_up(27)

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

        # Play the recording list
        elif self.key_mappings[index] == 'play':
            # if any channels are not recording or player play
            if not self.player.recording and not self.player.playing:
                self.player.play_all()

        # Switch up a channel
        elif self.key_mappings[index] == 'channel_up':
            self.event_handler.switch_channel(self.current_channel_index[0] + 1)

        # Switch down a channel
        elif self.key_mappings[index] == 'channel_down':
            self.event_handler.switch_channel(self.current_channel_index[0] - 1)

    def key_up(self, index):
        # if shift is pressed
        if self.keyboard.shift:
            pass

        elif index < 24:
            self.channel.key_up(index)

        # record function
        elif self.key_mappings[index] == 'record':
            if not self.player.recording and not self.player.playing:
                self.player.record()

                # plays all channels
                self.player.play_all()

        elif self.key_mappings[index] == 'stop':
            self.player.stop_all()
