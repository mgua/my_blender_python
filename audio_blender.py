#! python for blender
# Blender 4.3 code to receive input from the microphone and
# dynamically change a 3d object in a scene
#
# Marco Guardigli, mgua@tomware.it jan 01 2025
#
# see https://github.com/mgua/my_blender_python
#
# BEWARE!! this currently crashed blender after a few secs. 
# !! to be debugged !!
#
#


import bpy
import math
import struct
import wave
import sys
import numpy as np

# Import additional libraries for audio processing, via a custom import
sys.path.append(r"c:\Users\mgua\my_blender_4.3\packages")
import pyaudio


# Define constants
FORMAT = pyaudio.paInt16  # Audio format
CHANNELS = 1              # Number of channels (mono)
RATE = 44100              # Sample rate
CHUNK = 512               # Buffer size
THRESHOLD = 500           # Threshold for sound intensity

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open a stream to capture audio from the microphone
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

# Get the cube object (create one if it doesn't exist)
cube = bpy.data.objects.get("Cube")
if not cube:
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
    cube = bpy.context.object

def main():
    while True:
        # Read audio data from the stream
        data = stream.read(CHUNK)
        
        # Convert binary data to NumPy array of integers
        int_data = np.frombuffer(data, dtype=np.int16)
        
        # Calculate the root mean square (RMS) of the sound intensity
        rms = np.sqrt(np.mean(int_data ** 2))
        
        # Scale the size of the cube based on the RMS value
        if rms > THRESHOLD:
            cube.scale.x = 1 + (rms - THRESHOLD) / 5000.0
            cube.scale.y = 1 + (rms - THRESHOLD) / 5000.0
            cube.scale.z = 1 + (rms - THRESHOLD) / 5000.0
        else:
            cube.scale.x = 1
            cube.scale.y = 1
            cube.scale.z = 1

# Run the main loop in a separate thread to avoid blocking Blender's UI
import threading
threading.Thread(target=main).start()

# Clean up PyAudio stream and audio object when done
stream.stop_stream()
stream.close()
audio.terminate()


