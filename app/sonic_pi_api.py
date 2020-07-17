from pythonosc import udp_client
import time
import sys, os
import mido
import subprocess
from sf2utils.sf2parse import Sf2File



# Create a stream for controlling a synthesizer
class SynthStream(object):
    def __init__(self, stream_num, synth='piano', reverb=0.3):
        # Setup variables

        # Stream number
        self.stream = stream_num

        with open('/Users/ridvansong/Downloads/Part_1___2.sf2', 'rb') as sf2_file:
            sf2 = Sf2File(sf2_file)

        # List of synths
        self.synth_list = sf2.instruments

        # Reverb value
        self.reverb = reverb

        # Octave
        self.octave_shift = 0

        self.open_stream()

        time.sleep(0.1)
        mido_streams = mido.get_output_names()
        print(mido_streams)

        for i in mido_streams:
            if 'Synth' in i:
                port_num = i.split('(')[1].split(')')[0]
                print(port_num)
                break

        # Setup osc output
        self.port = mido.open_output()

    # Plays note
    def note_on(self, note):
        self.port.send(mido.Message('note_on', note=note))

    # Kills note
    def note_off(self, note):
        self.port.send(mido.Message('note_off', note=note))

    # Changes sound
    def change_synth(self, index):
        self.port.send(mido.Message('program_change', program=index))

    # Shift the octave
    def octave_shift(self, shift):
        self.octave_shift += shift
        self.sender.send_message('/python_out/%d/octave_shift' % self.stream, [self.octave_shift])

    def close_stream(self):
        os.system('cat sonic_pi_stop.txt | sonic_pi')

    def open_stream(self):
        print('openning stream')
        subprocess.Popen(['fluidsynth', '-a', 'portaudio', '-g', '5', '/Users/ridvansong/Downloads/Part_1___2.sf2'])

    # ---------------- Keyboard Interface ---------------------
    # Presses down a key
    def key_down(self, key_index):
        note = key_index + 60
        self.note_on(note)

    def key_up(self, key_index):
        note = key_index + 60
        self.note_off(note)
