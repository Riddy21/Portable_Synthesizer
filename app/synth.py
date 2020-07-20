import mido
from sf2utils.sf2parse import Sf2File

class Synth(object):
    @staticmethod
    def get_instruments():
        with open('/Users/ridvansong/Documents/OP-1 Project/app/Assets/Default.sf2', 'rb') as sf2_file:
            sf2 = Sf2File(sf2_file)
        return sf2.instruments

    def __init__(self, channel, port, mode='freeplay', instr=0, reverb=0.3, gain=270):
        # mode the synth is in
        self.mode = mode

        # set channel
        self.channel = channel

        # instrument index
        self.instr = instr

        # Effects
        self.reverb = reverb

        # Octave shift
        self.octave = 0

        self.port = port

    # Plays note
    def _note_on(self, note):
        self.port.send(mido.Message('note_on', note=note, channel=self.channel))

    # Kills note
    def _note_off(self, note):
        self.port.send(mido.Message('note_off', note=note, channel=self.channel))

    # Changes sound
    def _change_synth(self, index):
        self.port.send(mido.Message('program_change', program=index, channel=self.channel))

    # ---------------- Control Interface ---------------------
    # Presses down a key
    def key_down(self, key_index):
        note = key_index + self.octave + 60
        self._note_on(note)

    def key_up(self, key_index):
        note = key_index + self.octave + 60
        self._note_off(note)

    def change_synth(self, index):
        self.instr_ind = index
        self._change_synth(self.instr_ind)

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