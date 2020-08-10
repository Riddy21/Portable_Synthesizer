from start_server import start_server
import pygame as pg
from event_handler import EventHandler
from keyboard_driver import Keyboard
from gui import Gui
from threading_decorator import run_in_thread

@run_in_thread
def draw_interface_parallel(gui):
    while True:
        gui.draw_interface()

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

    # Start GUI and pass event_handler to look at events
    gui = Gui(event_handler)

    draw_interface_parallel(gui)

    while True:
        # Handle events
        event_handler.handle_events()

        # set framerate
        mainClock.tick(240)


if __name__ == '__main__':
    main()
