from pythonosc import udp_client
import time
import sys, os


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

        # Setup osc output
        self.sender = udp_client.SimpleUDPClient('127.0.0.1', 4560)
        self.sender.send_message('/python_out/%d/note_on' % self.stream, [60, 1])
        time.sleep(0.2)
        self.sender.send_message('/python_out/%d/note_on' % self.stream, [60, 1])

    # Plays note
    def note_on(self, note):
        self.sender.send_message('/python_out/%d/note_on' % self.stream, [note, 1])

    # Kills note
    def note_off(self, note):
        self.sender.send_message('/python_out/%d/note_on' % self.stream, [note, 0])

    # Changes sound
    def change_synth(self, index):
        self.sender.send_message('/python_out/%d/synth_change' % self.stream, [index])

    # Shift the octave
    def octave_shift(self, shift):
        self.octave_shift += shift
        self.sender.send_message('/python_out/%d/octave_shift' % self.stream, [self.octave_shift])

    def close_stream(self):
        os.system('cat sonic_pi_stop.txt | sonic_pi')

    def open_stream(self):
        os.system('cat sonic_pi_run_file.txt | sonic_pi')

    # ---------------- Keyboard Interface ---------------------
    # Presses down a key
    def key_down(self, key_index):
        note = key_index + 60
        self.note_on(note)

    def key_up(self, key_index):
        note = key_index + 60
        self.note_off(note)
