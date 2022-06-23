#include "sound2.c"
#include <chrono>
#include <thread>
#include <iostream>

using clock_type = std::chrono::high_resolution_clock;

int main(int argc, char *argv[])
{
    snd_pcm_t *handle;
    int err, morehelp;
    snd_pcm_hw_params_t *hwparams;
    snd_pcm_sw_params_t *swparams;
    int method = 0;
    signed short *samples;
    unsigned int chn;
    snd_pcm_channel_area_t *areas;
 
    snd_pcm_hw_params_alloca(&hwparams);
    snd_pcm_sw_params_alloca(&swparams);
 
    err = snd_output_stdio_attach(&output, stdout, 0);
    if (err < 0) {
        printf("Output failed: %s\n", snd_strerror(err));
        return 0;
    }
 
    printf("Playback device is %s\n", device);
    printf("Stream parameters are %uHz, %s, %u channels\n", rate, snd_pcm_format_name(format), channels);
    printf("Sine wave rate is %.4fHz\n", freq);
    printf("Using transfer method: %s\n", transfer_methods[method].name);
 
    if ((err = snd_pcm_open(&handle, device, SND_PCM_STREAM_PLAYBACK, 0)) < 0) {
        printf("Playback open error: %s\n", snd_strerror(err));
        return 0;
    }
    
    if ((err = set_hwparams(handle, hwparams, transfer_methods[method].access)) < 0) {
        printf("Setting of hwparams failed: %s\n", snd_strerror(err));
        exit(EXIT_FAILURE);
    }
    if ((err = set_swparams(handle, swparams)) < 0) {
        printf("Setting of swparams failed: %s\n", snd_strerror(err));
        exit(EXIT_FAILURE);
    }

 
    if (verbose > 0)
        snd_pcm_dump(handle, output);
 
    samples = malloc((period_size * channels * snd_pcm_format_physical_width(format)) / 8);
    if (samples == NULL) {
        printf("No enough memory\n");
        exit(EXIT_FAILURE);
    }
    
    areas = calloc(channels, sizeof(snd_pcm_channel_area_t));
    if (areas == NULL) {
        printf("No enough memory\n");
        exit(EXIT_FAILURE);
    }
    for (chn = 0; chn < channels; chn++) {
        areas[chn].addr = samples;
        areas[chn].first = chn * snd_pcm_format_physical_width(format);
        areas[chn].step = channels * snd_pcm_format_physical_width(format);
    }
 
    if (err < 0)
        printf("Transfer failed: %s\n", snd_strerror(err));

    unsigned char buffer[4410];
    for (int i=0; i<sizeof(buffer); i++) {
        buffer[i] = random() & 0xff;
    }

    auto when_started = clock_type::now(); 
    auto target_time = when_started + std::chrono::milliseconds(1000);
    int val;


    while (true){
        std::this_thread::sleep_until(target_time);
        val = snd_pcm_writei(handle, buffer, sizeof(buffer));
        target_time += std::chrono::milliseconds(1000/((int)44100/4410));
    }
    
    write_loop(handle, samples, areas);
 
    free(areas);
    free(samples);
    snd_pcm_close(handle);
    return 0;
}
