from sonic_pi_api import SynthStream
import time

def main():
    stream = SynthStream(stream=0)
    stream.open_stream()
    stream.note_on(60)
    stream.close_stream()


if __name__ == '__main__':
    main()