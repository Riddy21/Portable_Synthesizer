from sonic_pi_api import SynthStream
import time

def main():
    stream = SynthStream(stream=0)
    stream.open_stream()
    time.sleep(0.1)
    stream.note_on(60)
    time.sleep(0.1)
    stream.close_stream()


if __name__ == '__main__':
    main()