
# Interfacing with the Keyboard API
class Keyboard(object):
    def __init__(self, stream):
        # init the linked stream
        self.stream = stream

        # init key values
        self.keys = [True]*24

        # init analog knobs

        # init digital knobs

        # init stream for hooking up the button layouts

    # controls the keyboard to hit a key
    def key_down(self, key_index):
        if self.keys[key_index]:
            # toggle key
            self.keys[key_index] = False
            # play note
            self.stream.key_down(key_index)

    # controls the keyboard to release a key
    def key_up(self, key_index):
        # if is falling edge
        if not self.keys[key_index]:
            # toggle key
            self.keys[key_index] = True
            # play note
            self.stream.key_up(key_index)