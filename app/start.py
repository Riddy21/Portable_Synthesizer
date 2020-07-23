from start_server import start_server
import pygame as pg
from event_handler import EventHandler
from keyboard_driver import Keyboard
from gui import Gui

# Start program
def main():
    # Start the Fluidsynth server
    port = start_server(buffer_count=3, buffer_size=1024, sr=80000)

    # start pygame stuff
    pg.init()

    # Start Clock
    mainClock = pg.time.Clock()

    # Start playback controller and pass in the keyboard and the port
    event_handler = EventHandler(port=port)
    event_handler.add_channel(mode='freeplay')

    # Start GUI and pass event_handler to look at events
    gui = Gui(event_handler)

    while True:
        # Update GUI
        gui.draw_interface()

        # Handle events
        event_handler.handle_events()

        # set framerate
        mainClock.tick(240)


if __name__ == '__main__':
    main()
