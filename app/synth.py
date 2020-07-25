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

    def __init__(self, event_handler, instr=(0, 0), reverb=0.3, gain=270):
        # initialize variable from event handler
        self.channel_ind = event_handler.current_channel_index[0]
        self.port = event_handler.port

        # Recorder to keep track of notes
        self.recorder = event_handler.player

        # instrument index
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
        self.port.send(mido.Message('note_on', note=note, channel=self.channel_ind))

        if not background_mode:
            # Send time stamp and note to recorder
            self.recorder.record_event(time=time.time(), channel=self.channel_ind, event=['note_on', note])

    # Kills note
    def midi_note_off(self, note, background_mode=False):
        self.port.send(mido.Message('note_off', note=note, channel=self.channel_ind))

        if not background_mode:
            # Send time stamp and note to recorder
            self.recorder.record_event(time=time.time(), channel=self.channel_ind, event=['note_off', note])

    # Changes sound
    def midi_change_synth(self, bank, program, background_mode=False):
        # send message
        self.port.send(mido.Message('control_change', control=0, value=bank, channel=self.channel_ind))
        self.port.send(mido.Message('program_change', program=program, channel=self.channel_ind))

        # Change the self parameter
        self.instr = (bank, program)

        if not background_mode:
            # Send time stamp and note to recorder
            self.recorder.record_event(time=time.time(), channel=self.channel_ind,
                                       event=['synth_change', bank, program])

    @staticmethod
    def midi_stop(port):
        start = time.time()
        for note in range(128):
            for channel in range(16):
                port.send(mido.Message('note_off', note=note, channel=channel))
        end = time.time()
        print(end - start)

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
