from pythonosc import udp_client
import time
import sys, os


# Create a stream for controlling a synthesizer
class SynthStream(object):
    def __init__(self, stream, synth='piano', reverb=0.3):
        # Setup variables
        self.stream = stream
        self.synth = synth
        self.reverb = reverb

        # Setup osc output
        self.sender = udp_client.SimpleUDPClient('127.0.0.1', 4560)

    def note_on(self, note):
        self.sender.send_message('/python_out/%d/note_on' % self.stream, [note, 1])

    def note_off(self, note):
        self.sender.send_message('/python_out/%d/note_on' % self.stream, [note, 0])

    def change_synth(self, index):
        self.sender.send_message('/python_out/%d/synth_change' % self.stream, [index])

    def shift_octave(self, offset):
        self.sender.send_message('/python_out/%d/octave_shift' % self.stream, [offset])

    def close_stream(self):
        os.system('cat sonic_pi_stop.txt | sonic_pi')

    def open_stream(self):
        os.system('cat sonic_pi_run_file.txt | sonic_pi')
