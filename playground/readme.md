# Note to playground folder

This folder was used solely for testing purposes, there is no guarantee that any of these
files will work.

## game performance on different devices (pygame backends)

Through the devlopment of this game soham tested the game on a Macbook running the M2 chip. 
On the Mac the game was able to run with smooth 60fps but on his Lenovo Yoga running AMD Ryzen 5500U 
the game was only able to reach max of 30 fps. 

In any case the game was using up many system resources on both devices. We profiled on both devices (profilling section is on the 5500U).
There were some improvements to be made but still the fps would not go over 30.

We suspect this is due to pygame's nature of using the cpu to render rather than the gpu. Also the fact that python has a GIL forces the
threads to run in order than in paralel which is how the program is designed to run (with the chunks being mostly independent).
