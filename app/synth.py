import mido
import time
from sf2utils.sf2parse import Sf2File


class Synth(object):
    @staticmethod
    def get_instruments():
        file = open('Assets/Default.instrument_list.txt', 'r')
        instr_dict = dict()
        instr_str = file.read()

        # Make list into [bank, program, name]
        instr_str = instr_str.split('\n')
        for i in range(len(instr_str)):
            instr_str[i] = instr_str[i].split('-')

        # Pop empty item
        instr_str.pop()

        # Organize into dictionary
        for instr in instr_str:
            instr_dict[(int(instr[0]), int(instr[1]))] = instr[2]

        return instr_dict

    # Sends message to the corresponding channel
    @staticmethod
    def send_msg(channels, msg):
        channel = channels[msg.channel]

        channel.midi_send_msg(msg)

    @staticmethod
    def bytes2msg(bytes):
        return mido.Message.from_bytes(bytes)

    @staticmethod
    def midi_stop(port):
        # TODO: Find a more efficient way of turning off all on notes
        for note in range(128):
            for channel in range(16):
                port.send(mido.Message('note_off', note=note, channel=channel))

    def __init__(self, event_handler, instr=None, reverb=0.3, gain=270):
        # initialize variable from event handler
        if instr is None:
            instr = [0, 0]

        self.channel_ind = event_handler.current_channel_index[0]
        self.port = event_handler.port

        # Recorder to keep track of notes
        self.recorder = event_handler.player

        # instrument index [bank, program]
        self.instr = instr

        # Change the instrument to default
        self.change_synth(self.instr[0], self.instr[1])

        self.instr_dict = self.get_instruments()

        # Effects
        self.reverb = reverb

        # Octave shift
        self.octave = 0

    # Plays note
    def midi_note_on(self, note, background_mode=False):
        msg = mido.Message('note_on', note=note, channel=self.channel_ind)
        self.port.send(msg)

        # Send time stamp and note to recorder
        self.recorder.record_event(msg=msg.bytes(), time=time.time())

    # Kills note
    def midi_note_off(self, note, background_mode=False):
        msg = mido.Message('note_off', note=note, channel=self.channel_ind)
        self.port.send(msg)

        # Send time stamp and note to recorder
        self.recorder.record_event(msg=msg.bytes(), time=time.time())

    # Changes sound
    def midi_change_synth(self, bank, program):
        msg1 = mido.Message('control_change', control=0, value=bank, channel=self.channel_ind)
        msg2 = mido.Message('program_change', program=program, channel=self.channel_ind)
        # send message
        self.port.send(msg1)
        self.port.send(msg2)

        # Change the self parameter
        self.instr = [bank, program]

        # Send time stamp and note to recorder
        self.recorder.record_event(msg=msg1.bytes(), time=time.time())
        self.recorder.record_event(msg=msg2.bytes(), time=time.time() + 0.0001)

    # sends a midi message
    def midi_send_msg(self, msg):
        self.port.send(msg)

        # check for all the correspinding set values and change them
        if msg.type == 'control_change':
            self.instr[0] = msg.value
        elif msg.type == 'program_change':
            self.instr[1] = msg.program
        # TODO: add other possible controls

    # Records the initial information on instruments etc.
    def record_setup(self):
        msg1 = mido.Message('control_change', control=0, value=self.instr[0], channel=self.channel_ind)
        msg2 = mido.Message('program_change', program=self.instr[1], channel=self.channel_ind)

        # Sends the message with the time set as the original start time of the recording
        self.recorder.record_event(msg=msg1.bytes(), time=self.recorder.recording)
        self.recorder.record_event(msg=msg2.bytes(), time=self.recorder.recording + 0.0001)

    # ---------------- Control Interface ---------------------
    # Presses down a key
    def key_down(self, key_index):
        note = key_index + self.octave + 60
        self.midi_note_on(note)

    def key_up(self, key_index):
        note = key_index + self.octave + 60
        self.midi_note_off(note)

    def change_synth(self, bank, program):
        self.midi_change_synth(bank, program)

    def octave_shift(self, shift):
        self.octave += shift * 12

        # Return false if failed
        if self.octave < -60:
            self.octave = -60
            return False
        elif self.octave > 36:
            self.octave = 36
            return False
        return True
