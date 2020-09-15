import mido
import time

# TEMP for timing note hit
end = [0]

class Synth(object):
    @staticmethod
    def get_instruments():
        file = open('Assets/InstumentLists/Default.instrument_list.txt', 'r')
        instr_dict = dict()
        instr_str = file.read()

        # Make list into [bank, program, name]
        instr_str = list(instr_str.split('\n'))
        for i in range(len(instr_str)):
            instr_str[i] = instr_str[i].split('-')

        # Pop empty item
        instr_str.pop()

        # Organize into dictionary
        for instr in instr_str:
            instr_dict[(int(instr[0]), int(instr[1]))] = instr[2]

        return instr_dict

    # Sends message to the corresponding channel
    @staticmethod
    def send_msg(channels, msg):
        channel = channels[msg.channel]

        channel.midi_send_msg(msg)

    @staticmethod
    def bytes2msg(bytes):
        return mido.Message.from_bytes(bytes)

    @staticmethod
    def midi_stop(port):
        # TODO: Find a more efficient way of turning off all on notes
        for channel in range(16):
            msg = mido.Message('control_change', control=123, channel=channel)
            port.send(msg)

    def __init__(self,
                 event_handler,
                 channel_ind,
                 instr=(0,0),
                 volume=64,
                 modulation=0,
                 pitch=0,
                 balance=64,
                 pan=64,
                 sustain=False,
                 sustenuto=False,
                 reverb=0,
                 chorus=0,
                 velocity=64):

        self.channel_ind = channel_ind
        self.port = event_handler.port

        # Recorder to keep track of notes
        self.recorder = event_handler.player
        self.sustenuto_lock = event_handler.sustenuto_lock
        self.sustain_lock = event_handler.sustain_lock

        self.instr_dict = self.get_instruments()

        # Octave shift
        self.octave = 0

        # Effects init
        self.volume = None
        self.instr = None
        self.reverb = None
        self.modulation = None
        self.pitch = None
        self.balance = None
        self.pan = None
        self.sustain = None
        self.sustenuto = None
        self.reverb = None
        self.chorus = None
        self.velocity = None

        # Set default settings
        # Change the instrument to default
        self.change_synth(instr[0],instr[1])
        # Change the volume
        self.change_volume(volume)
        # Change Modulation
        self.change_modulation(modulation)
        # Change pitch
        self.change_pitch(pitch)
        # Change balance
        self.change_balance(balance)
        # Change pan
        self.change_pan(pan)
        # Change sustain
        self.change_sustain(sustain)
        # Change portamento
        self.change_sustenuto(sustenuto)
        # Change reverb
        self.change_reverb(reverb)
        # Change chorus
        self.change_chorus(chorus)
        # Change velocity
        self.change_velocity(velocity)

    # Plays note
    def midi_note_on(self, note):
        msg = mido.Message('note_on', note=note, velocity=self.velocity, channel=self.channel_ind)
        end[0] = time.time()
        #print(msg)
        self.port.send(msg)

        # Send time stamp and note to recorder
        self.recorder.record_event(msg=msg.bytes(), time=time.time())

    # Kills note
    def midi_note_off(self, note):
        msg = mido.Message('note_off', note=note, channel=self.channel_ind)
        self.port.send(msg)

        # Send time stamp and note to recorder
        self.recorder.record_event(msg=msg.bytes(), time=time.time())

    # Changes sound
    def midi_change_synth(self, bank, program):
        msg1 = mido.Message('control_change', control=0, value=bank, channel=self.channel_ind)
        msg2 = mido.Message('program_change', program=program, channel=self.channel_ind)
        # send message
        self.port.send(msg1)
        self.port.send(msg2)

        # Send time stamp and msg to recorder
        self.recorder.record_event(msg=msg1.bytes(), time=time.time())
        # 0.0001 is needed to make sure it comes after the control change but still stay instantly after
        self.recorder.record_event(msg=msg2.bytes(), time=time.time() + 0.0001)

    # Change volume
    def midi_change_volume(self, volume):
        msg = mido.Message('control_change', control=7, value=volume, channel=self.channel_ind)
        # send message
        self.port.send(msg)

        # Send time stamp and message to recorder
        self.recorder.record_event(msg=msg.bytes(), time=time.time())

    # Modulate
    def midi_change_modulation(self, modulation):
        msg = mido.Message('control_change', control=1, value=modulation, channel=self.channel_ind)
        # send message
        self.port.send(msg)

        # Send time stamp and message to recorder
        self.recorder.record_event(msg=msg.bytes(), time=time.time())

    # Pitch bend
    def midi_change_pitch(self, pitch):
        msg = mido.Message('pitchwheel', pitch=pitch, channel=self.channel_ind)
        # send message
        self.port.send(msg)

        # Send time stamp and message to recorder
        self.recorder.record_event(msg=msg.bytes(), time=time.time())

    # Balance
    def midi_change_balance(self, balance):
        msg = mido.Message('control_change', control=8, value=balance, channel=self.channel_ind)
        # send message
        self.port.send(msg)

        # Send time stamp and message to recorder
        self.recorder.record_event(msg=msg.bytes(), time=time.time())
        
    # Pan
    def midi_change_pan(self, pan):
        msg = mido.Message('control_change', control=10, value=pan, channel=self.channel_ind)
        # send message
        self.port.send(msg)

        # Send time stamp and message to recorder
        self.recorder.record_event(msg=msg.bytes(), time=time.time())

    # Sustain
    def midi_change_sustain(self, sustain):
        msg = mido.Message('control_change', control=64, value=sustain, channel=self.channel_ind)
        # send message
        self.port.send(msg)

        # Send time stamp and message to recorder
        self.recorder.record_event(msg=msg.bytes(), time=time.time())

    def midi_change_sustenuto(self, sustenuto):
        msg = mido.Message('control_change', control=66, value=sustenuto, channel=self.channel_ind)

        # send message
        self.port.send(msg)

        # Send time stamp and message to recorder
        self.recorder.record_event(msg=msg.bytes(), time=time.time()) 

    def midi_change_reverb(self, reverb):
        msg = mido.Message('control_change', control=91, value=reverb, channel=self.channel_ind)

        # send message
        self.port.send(msg)

        # Send time stamp and message to recorder
        self.recorder.record_event(msg=msg.bytes(), time=time.time())

    def midi_change_chorus(self, chorus):
        msg = mido.Message('control_change', control=93, value=chorus, channel=self.channel_ind)

        # send message
        self.port.send(msg)

        # Sent time stamp and message to recorder
        self.recorder.record_event(msg=msg.bytes(), time=time.time())

    # sends a midi message
    def midi_send_msg(self, msg):
        self.port.send(msg)
        #print(msg)

        # check for all the correspinding set values and change them
        if msg.type == 'note_on':
            self.velocity = msg.velocity
        elif msg.type == 'control_change':
            if msg.control == 0:
                self.instr[0] = msg.value
            elif msg.control == 7:
                self.volume = msg.value
            elif msg.control == 1:
                self.modulation = msg.value
            elif msg.control == 8:
                self.balance = msg.value
            elif msg.control == 10:
                self.pan = msg.value
            elif msg.control == 64:
                self.sustain = msg.value
                # For setting the channel locks when sustain gets changed
                if msg.value == 64:
                    self.sustain_lock[self.channel_ind] = True
                else:
                    self.sustain_lock[self.channel_ind] = False
            elif msg.control == 66:
                self.sustenuto = msg.value
                # Same as 6 lines above
                if msg.value == 64:
                    self.sustenuto_lock[self.channel_ind] = True
                else:
                    self.sustenuto_lock[self.channel_ind] = False
            elif msg.control == 91:
                self.reverb = msg.value
            elif msg.control == 93:
                self.chorus = msg.value
        elif msg.type == 'program_change':
            self.instr[1] = msg.program
        elif msg.type == 'pitchwheel':
            self.pitch = msg.pitch

    # Records the initial information on instruments volume etc
    def record_setup(self):
        msgs = [mido.Message('control_change', control=0, value=self.instr[0], channel=self.channel_ind),
                mido.Message('program_change', program=self.instr[1], channel=self.channel_ind),
                mido.Message('control_change', control=7, value=self.volume, channel=self.channel_ind),
                mido.Message('control_change', control=1, value=self.modulation, channel=self.channel_ind),
                mido.Message('pitchwheel', pitch=self.pitch, channel=self.channel_ind),
                mido.Message('control_change', control=8, value=self.balance, channel=self.channel_ind),
                mido.Message('control_change', control=10, value=self.pan, channel=self.channel_ind),
                mido.Message('control_change', control=64, value=self.sustain, channel=self.channel_ind),
                mido.Message('control_change', control=66, value=self.sustenuto, channel=self.channel_ind),
                mido.Message('control_change', control=91, value=self.reverb, channel=self.channel_ind),
                mido.Message('control_change', control=93, value=self.chorus, channel=self.channel_ind)
                ]

        # Sends the message with the time set as the original start time of the recording
        counter = -10
        for msg in msgs:
            self.recorder.record_event(msg=msg.bytes(), time=self.recorder.recording + counter)
            counter += 0.00001

    # ---------------- Control Interface ---------------------
    # Presses down a key
    def key_down(self, key_index):
        note = key_index + self.octave + 60
        self.midi_note_on(note)

    def key_up(self, key_index):
        note = key_index + self.octave + 60
        self.midi_note_off(note)

    def change_synth(self, bank, program):
        # Change the self parameter
        self.instr = [bank, program]
        # Send message
        self.midi_change_synth(bank, program)

    def change_volume(self, volume):
        if 128 > volume >= 0:
            # Change the self paramter
            self.volume = volume
            # Send message
            self.midi_change_volume(self.volume)

    def increment_volume(self, increment):
        volume_buff = self.volume + increment
        self.change_volume(volume_buff)
        print('volume: %s' % self.volume)

    def change_modulation(self, mod):
        if 128 > mod >= 0:
            self.modulation = mod
            self.midi_change_modulation(mod)

    def increment_modulation(self, increment):
        mod_buff = self.modulation + increment
        self.change_modulation(mod_buff)
        print('modulation: %s' % self.modulation)

    def change_pitch(self, pitch):
        if 8191 >= pitch >= -8192:
            self.pitch = pitch
            self.midi_change_pitch(pitch)

    def increment_pitch(self, increment):
        pitch_buff = self.pitch + increment
        self.change_pitch(pitch_buff)
        print('pitch: %s' % self.pitch)

    def change_balance(self, balance):
        if 128 > balance >= 0:
            self.balance = balance
            self.midi_change_balance(balance)

    def increment_balance(self, increment):
        bal_buff = self.balance + increment
        self.change_balance(bal_buff)
        print('balance: %s' % self.balance)

    def change_pan(self, pan):
        if 128 > pan >= 0:
            self.pan = pan
            self.midi_change_pan(pan)
            
    def increment_pan(self, increment):
        pan_buff = self.pan + increment
        self.change_pan(pan_buff)
        print('pan: %s' % self.pan)

    # True or False
    def change_sustain(self, sustain):
        if sustain:
            self.sustain = 64
            self.midi_change_sustain(64)
        else:
            self.sustain = 63
            self.midi_change_sustain(63)
    
    def toggle_sustain(self):
        if self.sustain == 63:
            self.sustain = 64
            self.midi_change_sustain(64)
        else:
            self.sustain = 63
            self.midi_change_sustain(63)

    # True or False
    def change_sustenuto(self, sustenuto):
        if sustenuto:
            self.sustenuto = 64
            self.midi_change_sustenuto(64)
        else:
            self.sustenuto = 63
            self.midi_change_sustenuto(63)

    def toggle_sustenuto(self):
        if self.sustenuto == 63:
            self.sustenuto = 64
            self.midi_change_sustenuto(64)
        else:
            self.sustenuto = 63
            self.midi_change_sustenuto(63)

    def change_reverb(self, reverb):
        if 128 > reverb >= 0:
            self.reverb = reverb
            self.midi_change_reverb(reverb)

    def increment_reverb(self, increment):
        rev_buff = self.reverb + increment
        self.change_reverb(rev_buff)
        print('reverb: %s' % self.reverb)

    def change_chorus(self, chorus):
        if 128 > chorus >= 0:
            self.chorus = chorus
            self.midi_change_chorus(chorus)
    
    def increment_chorus(self, increment):
        cho_buff = self.chorus + increment
        self.change_chorus(cho_buff)
        print('chorus: %s' % self.chorus)

    def change_velocity(self, velocity):
        if 128 > velocity >= 0:
            self.velocity = velocity

    def increment_velocity(self, increment):
        vel_buff = self.velocity + increment
        self.change_velocity(vel_buff)
        print('velocity: %s' % self.velocity)

    def octave_shift(self, shift):
        self.octave += shift * 12

        # Return false if failed
        if self.octave < -60:
            self.octave = -60
            return False
        elif self.octave > 36:
            self.octave = 36
            return False
        return True
