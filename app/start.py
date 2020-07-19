from engine import Engine

# Start program
def main():
    # Start the Fluidsynth server
    port = Engine.start_server(buffer_count=3, buffer_size=1024, sr=48000)

    # Start the program
    Engine(port)
    pass

if __name__ == '__main__':
    main()
