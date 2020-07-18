import time
import sys, os
import mido
import subprocess
from sf2utils.sf2parse import Sf2File
import threading

# Fluid synth settings
BUFFER_COUNT= 3
BUFFER_SIZE = 1024
SR = 48000

# Opens the Fluid synth stream for playing notes
def open_stream():
    print('openning stream')
    subprocess.Popen(['fluidsynth', '-a', 'portaudio', '-c', str(BUFFER_COUNT), '-z', str(BUFFER_SIZE), '-r', str(SR), '-g', '5',
                      '/Users/ridvansong/Documents/OP-1 Project/app/Assets/Part_1___2.sf2'])
    mido_streams = mido.get_output_names()
    print(mido_streams)

    for i in mido_streams:
        if 'Synth' in i:
            port_num = i.split('(')[1].split(')')[0]
            print(port_num)
            break

    # Setup stream output
    port = mido.open_output()
    return port


# Create a stream for controlling a synthesizer
class Synth(object):
    def __init__(self, channel, port, instr=0, synth='piano', reverb=0.3):
        # Setup variables

        # Stream number
        self.channel = channel

        # Instruments
        with open('/Users/ridvansong/Documents/OP-1 Project/app/Assets/Part_1___2.sf2', 'rb') as sf2_file:
            sf2 = Sf2File(sf2_file)
        self.instr_list = sf2.instruments
        self.instr_ind = instr

        # Reverb value
        self.reverb = reverb

        # Octave
        self.octave_shift = 0


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

    # Shift the octave
    def _octave_shift(self, shift):
        self.octave_shift += shift

    # ---------------- Keyboard Interface ---------------------
    # Presses down a key
    def key_down(self, key_index):
        note = key_index + 60
        self._note_on(note)

    def key_up(self, key_index):
        note = key_index + 60
        self._note_off(note)

    def use_knob(self, index, knob_num):
        if knob_num == 0:
            self.instr_ind = index
            self._change_synth(self.instr_ind)
