import pvporcupine
import pyaudio
import struct
from engine.command import allCommands

def hotword_detect():
    porcupine = pvporcupine.create(
        keywords=["computer"]  # 👈 using built-in keyword
    )

    pa = pyaudio.PyAudio()
    stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )

    print("🟢 Hotword listening (say 'computer')")

    while True:
        pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

        if porcupine.process(pcm) >= 0:
            print("🔥 Hotword detected")
            allCommands()


