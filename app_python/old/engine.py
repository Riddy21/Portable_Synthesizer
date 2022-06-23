import mido
import subprocess
import time
import platform
import os
import pygame as pg
from keyboard_driver import Keyboard
from event_handler import EventHandler
from gui import Gui

# Engine class, handles all events, where main loop is
# noinspection PyUnresolvedReferences
class Engine(object):


    def __init__(self, port):
        # start pygame stuff
        pg.init()

        # Start Clock
        self.mainClock = pg.time.Clock()

        # Connect to Fluidsynth
        self.port = port

        # Get keyboard
        self.keyboard = Keyboard()

        # Start playback controller and pass in the keyboard and the port
        self.event_handler = EventHandler(self)
        self.event_handler.add_channel(mode='freeplay')

        # Start GUI
        self.gui = Gui(self.playback_handler)

        self._loop()

    # loop
    def _loop(self):
        while True:
            # Update GUI
            self.gui.draw_interface()

            # Handle events
            self.event_handler.handle_events()

            # set framerate
            self.mainClock.tick(240)