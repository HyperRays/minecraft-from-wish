import logging
import queue  # Python 3.x
import sys
import threading
from multiprocessing import Process
import time
import sounddevice as sd
import soundfile as sf

buffersize = 20

__q = queue.Queue(maxsize=buffersize)
__event = threading.Event()

# https://python-sounddevice.readthedocs.io/en/0.4.5/examples.html#play-a-very-long-sound-file
def _play_sound(file, device = None,blocksize = 2048):
    def callback(outdata, frames, time, status):
        assert frames == blocksize
        if status.output_underflow:
            print('Output underflow: increase blocksize?', file=sys.stderr)
            raise sd.CallbackAbort
        assert not status
        try:
            data = __q.get_nowait()
        except queue.Empty:
            print('Buffer is empty: increase buffersize?', file=sys.stderr)
            raise sd.CallbackAbort
        if len(data) < len(outdata):
            outdata[:len(data)] = data
            outdata[len(data):] = b'\x00' * (len(outdata) - len(data))
            raise sd.CallbackStop
        else:
            outdata[:] = data



    try:
        with sf.SoundFile(file) as f:
            for _ in range(buffersize):
                data = f.buffer_read(blocksize, dtype='float32')
                if not data:
                    break
                __q.put_nowait(data)  # Pre-fill queue

            stream = sd.RawOutputStream(
                samplerate=f.samplerate, blocksize=blocksize,
                device=device, channels=f.channels, dtype='float32',
                callback=callback, finished_callback=__event.set)
            with stream:
                timeout = blocksize * buffersize / f.samplerate
                while data:
                    data = f.buffer_read(blocksize, dtype='float32')
                    __q.put(data, timeout=timeout)
                __event.wait()  # Wait until playback is finished
    except queue.Full:
        logging.error("Music player buffer/queue full")

class SoundManager():

    def __init__(self):
        self.sound_files: dict[str, str] = dict() 
        self.running_instances: dict[str, Process] = dict()


    def load_sound(self, path, name):
        self.sound_files.update({name: path})
        

    def play_sound(self, name) -> str:
        unique_name = name + str(time.time()) 
        self.running_instances[unique_name] = Process(target = _play_sound, args = (self.sound_files[name],), daemon = True)
        self.running_instances[unique_name].start()
        return unique_name
        
    def update(self):
        for key,value in self.running_instances.items():
            if not value.is_alive():
                del self.running_instances[key]
        
