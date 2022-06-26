import Foundation

print("hello")
Synth.shared.setWaveformTo(Oscillator.whiteNoise)
Synth.shared.volume = 0.5

sleep(5)
