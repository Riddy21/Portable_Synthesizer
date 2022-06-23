#include "config.h"
#include "synthAPI.h"
#include "audioOut.h"

#include <stdio.h>
#include <vector>
#include <cmath>
#include <GL/glut.h>
#include <thread>
#include <iostream>
#include <limits>
#include <semaphore.h>

int test=0;
long loop_counter = 0;
float data_in_l[BLOCK_SIZE];
float data_in_r[BLOCK_SIZE];
//sem_t audio_mutex;
//sem_t synth_mutex;

void processNormalKeys(unsigned char key, int x, int y) {
    test = !test;    
}

void audio_thread(){
    start_pcm();
    while(1){
        //sem_wait(&audio_mutex);
        //sem_post(&synth_mutex);
        loop_counter += 1;
        stream(data_in_l, data_in_r);
    }
    end_pcm();
}

void synth_thread(){
    while(1){
        //sem_wait(&synth_mutex);
        for (int i=0; i<BLOCK_SIZE; i++){
            if (test){
                data_in_l[i] = std::sin((2.0*PI/SAMPLE_RATE)*(((double)i + (double)loop_counter*BLOCK_SIZE)*261.63*std::pow(2.0, 4.0/12.0)));
                data_in_r[i] = std::sin((2.0*PI/SAMPLE_RATE)*(((double)i + (double)loop_counter*BLOCK_SIZE)*261.63*std::pow(2.0, 0.0/12.0)));
            } else {
                data_in_l[i] = 0;
                data_in_r[i] = 0;
            }
        }
        for (int i=0; i<BLOCK_SIZE; i++){
            if (test){
                data_in_l[i] = std::sin((2.0*PI/SAMPLE_RATE)*(((double)i + (double)loop_counter*BLOCK_SIZE)*261.63*std::pow(2.0, 4.0/12.0)));
                data_in_r[i] = std::sin((2.0*PI/SAMPLE_RATE)*(((double)i + (double)loop_counter*BLOCK_SIZE)*261.63*std::pow(2.0, 0.0/12.0)));
            } else {
                data_in_l[i] = 0;
                data_in_r[i] = 0;
            }
        }
        //sem_post(&audio_mutex);
    }
}

int main(int argc, char *argv[]){

    //glutInit(&argc, argv);
    //glutInitWindowSize (300,300);
    //glutCreateWindow ("OpenGL / C Example - Well House");
    //glutKeyboardFunc(processNormalKeys);
    //
    //sem_init(&audio_mutex, 0, 0);
    //sem_init(&synth_mutex, 0, 1);

    std::thread synth_thread_inst = std::thread(synth_thread);
    std::thread audio_thread_inst = std::thread(audio_thread);

    for(int j=0; j<20; j++){
        sleep(1);
        printf("%d\n", j);
        test = !test;
    }

    synth_thread_inst.join();
    audio_thread_inst.join();

    //glutMainLoop();
    //for (int j=0; j<3*100; j++){
    //    double sound_r [AUDIO_BLOCK_SIZE];
    //    for (int i=0; i<AUDIO_BLOCK_SIZE; i++){
    //        sound_r[i] = std::sin((2.0*PI/SAMPLE_RATE)*(((double)i + (double)j*AUDIO_BLOCK_SIZE)*261.63))/3.0;
    //        sound_r[i] += std::sin((2.0*PI/SAMPLE_RATE)*(((double)i + (double)j*AUDIO_BLOCK_SIZE)*261.63*std::pow(2.0, 4.0/12.0)))/3.0;
    //        sound_r[i] += std::sin((2.0*PI/SAMPLE_RATE)*(((double)i + (double)j*AUDIO_BLOCK_SIZE)*261.63*std::pow(2.0, 7.0/12.0)))/3.0;
    //    }

    //    writeStereoStdoutBlockData(sound_r, sound_r);
    //}


    return 0;
}
