import mido
import time
from sf2utils.sf2parse import Sf2File

class Synth(object):
    @staticmethod
    def get_instruments():
        with open('/Users/ridvansong/Documents/OP-1 Project/app/Assets/Default.sf2', 'rb') as sf2_file:
            sf2 = Sf2File(sf2_file)
        return sf2.instruments

    def __init__(self, channel, port, recorder, mode='freeplay', instr=0, reverb=0.3, gain=270):
        # mode the synth is in
        self.mode = mode

        # set channel
        self.channel = channel

        # instrument index
        self.instr = instr

        self.instr_list = self.get_instruments()

        # Effects
        self.reverb = reverb

        # Octave shift
        self.octave = 0

        self.port = port

        # Recorder to keep track of notes
        self.recorder = recorder

    # Plays note
    def midi_note_on(self, note, background_mode=False):
        self.port.send(mido.Message('note_on', note=note, channel=self.channel))

        if not background_mode:
            # Send time stamp and note to recorder
            self.recorder.record_event(time=time.time(), channel=self.channel, event=['note_on', note])

    # Kills note
    def midi_note_off(self, note, background_mode=False):
        self.port.send(mido.Message('note_off', note=note, channel=self.channel))

        if not background_mode:
            # Send time stamp and note to recorder
            self.recorder.record_event(time=time.time(), channel=self.channel, event=['note_off', note])

    # Changes sound
    def midi_change_synth(self, index, background_mode=False):
        if index < 0 or index >127:
            return
        # send message
        self.port.send(mido.Message('program_change', program=index, channel=self.channel))

        # Change the self parameter
        self.instr = index

        if not background_mode:
            # Send time stamp and note to recorder
            self.recorder.record_event(time=time.time(), channel=self.channel, event=['program_change', index])

    @staticmethod
    def midi_stop(port):
        start = time.time()
        for note in range(128):
            for channel in range(16):
                port.send(mido.Message('note_off', note=note, channel=channel))
        end = time.time()
        print(end-start)

    # ---------------- Control Interface ---------------------
    # Presses down a key
    def key_down(self, key_index):
        note = key_index + self.octave + 60
        self.midi_note_on(note)

    def key_up(self, key_index):
        note = key_index + self.octave + 60
        self.midi_note_off(note)

    def change_synth(self, index):
        self.midi_change_synth(index)

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