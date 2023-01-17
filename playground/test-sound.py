# from the https://python-sounddevice.readthedocs.io/en/0.3.12/examples.html#play-a-sound-file docs and other docs about the same thing
"""Play an audio file using a limited amount of memory.

The soundfile module (http://PySoundFile.rtfd.io/) must be installed for
this to work.  NumPy is not needed.

In contrast to play_file.py, which loads the whole file into memory
before starting playback, this example program only holds a given number
of audio blocks in memory and is therefore able to play files that are
larger than the available RAM.

"""
import queue  # Python 3.x
import sys
import threading
from multiprocessing import Process
import sounddevice as sd
import soundfile as sf

from time import sleep


buffersize = 20

__q = queue.Queue(maxsize=buffersize)
__event = threading.Event()

file = "../assets/audio/Track_1.1.wav"
file2 = "../assets/audio/Track_1.2.wav"



p = Process(target=play_sound, args=(file, ), daemon=True)
# p2 = Process(target=play_sound, args=(file2, ))
if __name__ == '__main__':
    p.start()
    # p2.start()
    print("hello")

        
        # if p2.is_alive():
        #     sleep(1)
        # else:
        #     print("hi")
        #     p.join()
        #     break