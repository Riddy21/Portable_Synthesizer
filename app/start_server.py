import mido
import os
import sys
import platform
import time
import subprocess


# starts the server before running the Engine
def start_server(buffer_count, buffer_size, sr):
    print('INFO: Opening stream')

    # get assets directory
    home_path = os.getcwd()
    assets_path = os.path.join(home_path, 'Assets', 'SoundFonts', 'Default.sf2')

    # Change audio channel
    if platform.system() == 'Darwin' or platform.system() == 'Windows':
        audio = 'portaudio'
    else:
        audio = 'alsa'

    subprocess.Popen(
        ['fluidsynth', '-a', audio, '-c', str(buffer_count), '-z', str(buffer_size), '-r', str(sr), '-g', '5',
         assets_path])
    #
    # subprocess.Popen(
    #     ['fluidsynth', '-a', audio, '-g', '5',
    #      assets_path])

    time.sleep(1)

    mido_streams = mido.get_output_names()
    print('INFO: Streams: %s' % mido_streams)

    # Setup stream output
    if platform.system() == 'Darwin' or platform.system() == 'Windows':
        port = mido.open_output()
    else:
        port = False
        # Find port number
        for i in mido_streams:
            if 'Synth' in i:
                port_num = i.split('(')[1].split(')')[0]
                port = mido.open_output('Synth input port (%s:0)' % port_num)
                break

    if port:
        print('INFO: Established Fluidsynth connection on port %s' % port)
    else:
        print('ERROR: Cannot connect to port')
        sys.exit(2)
    return port
