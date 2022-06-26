import Foundation
import AVFoundation

// Input float represents time and output float is audio
typealias Signal = (Float) -> (Float)

struct Oscillator {
    static var amplitude: Float = 1
    static var frequency: Float = 440

    static let sine = { (time: Float) -> Float in
        return Oscillator.amplitude * sin(2.0 * Float.pi * Oscillator.frequency * time)
    }

    static let triangle = { (time: Float) -> Float in
        let period = 1.0 / Double(Oscillator.frequency)
        let currentTime = fmod(Double(time), period)
        let value = currentTime / period


        var result = 0.0
        if value < 0.25 {
            result = value * 4
        } else if value < 0.75 {
            result = 2.0 - (value * 4.0)
        } else {
            result = value * 4 - 4.0
        }


        return Oscillator.amplitude * Float(result)
    }

    static let sawtooth = { (time: Float) -> Float in
        let period = 1.0 / Oscillator.frequency
        let currentTime = fmod(Double(time), Double(period))
        return Oscillator.amplitude * ((Float(currentTime) / period) * 2 - 1.0)
    }

    static let square = { (time: Float) -> Float in
        let period = 1.0 / Double(Oscillator.frequency)
        let currentTime = fmod(Double(time), period)
        return ((currentTime / period) < 0.5) ? Oscillator.amplitude : -1.0 * Oscillator.amplitude
    }

    static let whiteNoise = { (time: Float) -> Float in
        return Oscillator.amplitude * Float.random(in: -1...1)
    }
}

class Synth {
    // Properties
    public static let shared = Synth()

    public var volume: Float {
        set {
            audioEngine.mainMixerNode.outputVolume = newValue
        }
        get {
            return audioEngine.mainMixerNode.outputVolume
        }
    }
    private var audioEngine: AVAudioEngine
    private var time: Float = 0
    private let sampleRate: Double
    private let deltaTime: Float
    
    private lazy var sourceNode = AVAudioSourceNode { (_, _, frameCount, audioBufferList) -> OSStatus in
        let ablPointer = UnsafeMutableAudioBufferListPointer(audioBufferList)
        for frame in 0..<Int(frameCount) {
            let sampleVal = self.signal(self.time)
            self.time += self.deltaTime
            for buffer in ablPointer {
                let buf: UnsafeMutableBufferPointer<Float> = UnsafeMutableBufferPointer(buffer)
                buf[frame] = sampleVal
            }
            // NOTE: JUST FOR left ear
            //UnsafeMutableBufferPointer(ablPointer[0])[frame] = sampleVal
            // NOTE: JUST FOR right ear
            //UnsafeMutableBufferPointer(ablPointer[1])[frame] = sampleVal
        }
        return noErr
    }

    private var signal: Signal

    // Constructor
    init(signal: @escaping Signal = Oscillator.sine) {
        audioEngine = AVAudioEngine()

        let mainMixer = audioEngine.mainMixerNode
        let outputNode = audioEngine.outputNode
        let format = outputNode.inputFormat(forBus: 0)

        sampleRate = format.sampleRate
        deltaTime = 1 / Float(sampleRate)

        self.signal = signal

        let inputFormat = AVAudioFormat(commonFormat: format.commonFormat, sampleRate: sampleRate, channels: 2, interleaved: format.isInterleaved)
        audioEngine.attach(sourceNode)
        audioEngine.connect(sourceNode, to: mainMixer, format: inputFormat)
        audioEngine.connect(mainMixer, to: outputNode, format: nil)
        mainMixer.outputVolume = 0
        do {
           try audioEngine.start()
        } catch {
           print("Could not start engine: \(error.localizedDescription)")
        }
    }

    // Public functions
    public func setWaveformTo(_ signal: @escaping Signal) {
        self.signal = signal
    }

}
