#ifndef AUDIO_OUT_H
#define AUDIO_OUT_H

#include "config.h"
#include <stdio.h>
#include <iostream>
#include <string.h>
#include <sched.h>
#include <errno.h>
#include <getopt.h>
#include "alsa/asoundlib.h"
#include <sys/time.h>
#include <math.h>
#include <limits>


void stream(float * data_in_l,
            float * data_in_r);
int start_pcm();
int end_pcm();

#endif
