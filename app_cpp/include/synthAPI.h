#ifndef SYNTH_API_H
#define SYNTH_API_H

#include "audioOut.h"
#include "config.h"
#include <chrono>
#include <thread>
#include <iostream>
#include <vector>

class SynthEngine{
    private:
        std::vector<double> m_notes;
        void update();
    public:
        bool test;

        SynthEngine();

        void start();
        void play(int note);
        void stop(int note);
};

#endif
