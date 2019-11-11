# soundplayer.py

import os
import threading


class SoundPlayer:
    '''
    Sound player based on SoX, called "the Swiss Army knife of sound processing programs" by its developper.
    This simple Python wrapper is based on Linux shell commands running in extra threads. 
    For the Raspberry Pi the following installation are needed:
    sudo apt-get install sox
    sudo apt-get install mp3
    '''
    @staticmethod
    def playTone(frequencies, duration, blocking = False, device = 0):
        '''
        Plays one or several sine tones with given frequencies and duration.
        @param frequencies: the frequency or a list of several frequencies in Hz
        @param duration: the duration in s
        @param blocking: if True, the functions blocks until playing is finished; otherwise it returns immediately (default: False)
        @param device: the sound device ID (e.g. 0: standard device, 1: USB sound adapter)
        '''
        if not type(frequencies) == list:
            frequencies = [frequencies]
        if blocking:
            SoundPlayer._emit(frequencies, duration, device)
        else:
            #thread.start_new_thread(SoundPlayer._emit, (frequencies, duration, device))
            threading.Thread(target=SoundPlayer._emit,
            args=(frequencies, duration, device),).start()

    # @staticmethod
    # def isPlaying():
    #     '''
    #     Checks if the sound is still playing.
    #     @return: True, if the sound is playing; otherwise False
    #     '''
    #     info = os.popen("ps -Af").read()
    #     process_count = info.count("play")
    #     return process_count >= 2

    @staticmethod
    def _emit(frequencies, duration, device):
        s = " "
        for f in frequencies:
            s += "sin " + str(f) + " "
        cmd = "AUDIODEV=hw:" + str(device) + " play -q -n synth " + str(duration) + \
            s + " 2> /dev/null" 
        os.system(cmd)
        
    def __init__(self, audiofile, device = 0):
        '''
        Creates a sound player to play the given audio file (wav, mp3, etc.) 
        to be played at given device ID. Throws exception, if the sound resource is not found.
        @param audiofile: the sound file to play
        @param device: the sound device ID (e.g. 0: standard device, 1: USB sound adapter)
        '''
        if not os.path.isfile(audiofile) :
            raise Exception("Audio resource " + audiofile + " not found")
        self.audiofile = audiofile
        self.device = device
 
    @staticmethod
    def _run(cmd):
        os.system(cmd)

    def play(self, volume = 1, blocking = False):
        '''
        Plays the sound with given volume (default: 1). The function returns immediately.
        @param volume: the sound level (default: 1)
        @param blocking: if True, the functions blocks until playing is finished; otherwise it returns immediately (default: False)
        '''
        self.volume = volume
        cmd = "AUDIODEV=hw:" + str(self.device) + \
            " play -v " + str(self.volume) + \
            " -q " + self.audiofile + " 2> /dev/null"

        if blocking:
            self._run(cmd)
        else:
            #thread.start_new_thread(SoundPlayer._run, (cmd,))
            threading.Thread(target=SoundPlayer._run,
            args=(cmd,),).start()

    def isPlaying(self):
        '''
        Checks if the sound is still playing.
        @return: True, if the sound is playing; otherwise False
        '''
        info = os.popen("ps -Af").read()
        process_count = info.count("play -v 1.0 -q " + self.audiofile)
        return process_count >= 2

    @staticmethod
    def stop():
        '''
        Stops playing.
        '''
        cmd = "sudo killall -9 play"
        #thread.start_new_thread(SoundPlayer._run, (cmd,))
        threading.Thread(target=SoundPlayer._run,
        args=(cmd,),).start()

    @staticmethod
    def pause():
        '''
        Pauses playing momentarily.
        '''
        cmd = "sudo pkill -STOP play"
        #thread.start_new_thread(SoundPlayer._run, (cmd,))
        threading.Thread(target=SoundPlayer._run,
        args=(cmd,),).start()
    

    @staticmethod
    def resume():
        '''
        Resumes playing (after it has been stopped).
        '''
        cmd = "sudo pkill -CONT play"
        #thread.start_new_thread(SoundPlayer._run, (cmd,))
        threading.Thread(target=SoundPlayer._run,
        args=(cmd,),).start()
