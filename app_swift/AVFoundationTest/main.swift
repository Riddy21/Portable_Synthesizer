import Foundation

print("hello")
Synth.shared.setWaveformTo(Oscillator.sine)
Synth.shared.volume = 0.5

sleep(5)
