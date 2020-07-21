import mido
import subprocess
import time
import platform
import os
import pygame as pg
from keyboard_driver import Keyboard
from playback_handler import PlaybackHandler
from gui import GUI

# Engine class, handles all events, where main loop is
# noinspection PyUnresolvedReferences
class Engine(object):
    @staticmethod
    def start_server(buffer_count, buffer_size, sr):
        print('INFO: Opening stream')

        # get assets directory
        home_path = os.getcwd()
        assets_path = os.path.join(home_path, 'Assets', 'Default.sf2')

        # Change audio channel
        if platform.system() == 'Darwin' or platform.system() == 'Windows':
            audio = 'portaudio'
        else:
            audio = 'alsa'

        subprocess.Popen(
            ['fluidsynth', '-a', audio, '-c', str(buffer_count), '-z', str(buffer_size), '-r', str(sr), '-g', '5',
             assets_path])

        time.sleep(5)

        mido_streams = mido.get_output_names()
        print('INFO: Streams: %s' % mido_streams)

        # Setup stream output
        if platform.system() == 'Darwin' or platform.system() == 'Windows':
            port = mido.open_output()
        else:
            # Find port number
            for i in mido_streams:
                if 'Synth' in i:
                    port_num = i.split('(')[1].split(')')[0]
                    break
            port = mido.open_output('Synth input port (%s:0)' % port_num)

        print('INFO: Established Fluidsynth connection on port %s' % port)
        return port

    def __init__(self, port):
        # start pygame stuff
        pg.init()

        # Start Clock
        self.mainClock = pg.time.Clock()

        # Connect to Fluidsynth
        self.port = port

        # Get keyboard
        self.keyboard = Keyboard()

        # Start playback controller and pass in the keyboard
        self.playback_handler = PlaybackHandler(keyboard=self.keyboard)
        self.playback_handler.add_channel(mode='freeplay', port=self.port)

        # Start GUI
        self.gui = GUI(self.playback_handler)

        self.loop()

    # handle events
    def handle_events(self):
        start = time.time()
        events = pg.event.get()
        for e in events:
            if e.type == pg.KEYDOWN:
                try:
                    note = self.keyboard.key_dict[e.key]
                except KeyError:
                    pass
                else:
                    self.keyboard.key_down(note)
                    end = time.time()
                    # print(end-start)
            elif e.type == pg.KEYUP:
                try:
                    note = self.keyboard.key_dict[e.key]
                except KeyError:
                    pass
                else:
                    self.keyboard.key_up(note)

        knobs = self.keyboard.get_knobs()
        if knobs[0]:
            self.keyboard.use_knob(0)

    # loop
    def loop(self):
        while True:
            # Update GUI
            self.gui.draw_interface()

            # Handle events
            self.handle_events()

            self.mainClock.tick(240)