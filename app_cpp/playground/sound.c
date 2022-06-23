/*
 *  This extra small demo sends a random samples to your speakers.
 */
 
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sched.h>
#include <errno.h>
#include <getopt.h>
#include "alsa/asoundlib.h"
#include <sys/time.h>
#include <math.h>
 
static char *device = "default";            /* playback device */
int8_t buffer[256];              /* some random data */
int8_t buffer2[256];              /* some random data */
 
int main(void)
{
    int err;
    unsigned int i;
    snd_pcm_t *handle;
    snd_pcm_sframes_t frames;
 
    for (i = 0; i < sizeof(buffer); i++)
        buffer[i] = random() & 0xff;
    for (i = 0; i < sizeof(buffer); i++)
        buffer2[i] = 0;
 
 
    int counter = 0;
    while (true){
        if ((err = snd_pcm_open(&handle, device, SND_PCM_STREAM_PLAYBACK, 0)) < 0) {
            printf("Playback open error: %s\n", snd_strerror(err));
            exit(EXIT_FAILURE);
        }
        if ((err = snd_pcm_set_params(handle,
                          SND_PCM_FORMAT_S16_LE,
                          SND_PCM_ACCESS_RW_INTERLEAVED,
                          1,
                          51200,
                          1,
                          5000)) < 0) {   /* 0.05sec */
            printf("Playback open error: %s\n", snd_strerror(err));
            exit(EXIT_FAILURE);
        }
        while(true) {
            std::cout << "Testing\n";
            frames = snd_pcm_writei(handle, buffer, sizeof(buffer));
            if (counter > 1000){break;}

            if (frames < 0){
                frames = snd_pcm_recover(handle, frames, 0);
                counter += 1;
            }
            if (frames < 0) {
                printf("snd_pcm_writei failed: %s\n", snd_strerror(frames));
                break;
            }
            if (frames > 0 && frames < (long)sizeof(buffer)){
                printf("Short write (expected %li, wrote %li)\n", (long)sizeof(buffer), frames);
                counter = 0;
            }
        }
        /* pass the remaining samples, otherwise they're dropped in close */
        std::cout << "restarting\n";
        sleep(2);
        counter = 0;
        err = snd_pcm_drain(handle);
        if (err < 0)
            printf("snd_pcm_drain failed: %s\n", snd_strerror(err));
        snd_pcm_close(handle);
    }
 
    return 0;
}
