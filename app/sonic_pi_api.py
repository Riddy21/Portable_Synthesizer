from pythonosc import udp_client
import time
import sys, os
import mido
import subprocess


# Create a stream for controlling a synthesizer
class SynthStream(object):
    def __init__(self, stream_num, synth='piano', reverb=0.3):
        # Setup variables

        # Stream number
        self.stream = stream_num

        # List of synths
        self.synth_list = ['beep', 'blade', 'bnoise', 'chipbass', 'chiplead', 'chipnoise', 'cnoise', 'dark_ambience',
                           'dpulse', 'dsaw', 'dtri', 'dull_bell', 'fm', 'gnoise', 'growl', 'hollow', 'hoover',
                           'mod_beep', 'mod_dsaw', 'mod_fm,mod_pulse', 'mod_saw', 'mod_sine', 'mod_tri', 'noise',
                           'piano', 'pluck', 'pnoise', 'pretty_bell', 'prophet', 'pulse', 'saw', 'sine', 'sound_in',
                           'sound_in_stereo', 'square', 'subpulse', 'supersaw', 'tzb303', 'tech_saws']

        # index of the synth based on the input
        self.synth_index = self.synth_list.index(synth)

        # Reverb value
        self.reverb = reverb

        # Octave
        self.octave_shift = 0

        self.open_stream()

        time.sleep(0.1)
        print(mido.get_output_names())

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
