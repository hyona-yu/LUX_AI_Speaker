
import pyaudio
import numpy as np
import wave
import time
import sys
def after_lux():
    #CHUNK는 음성데이터를 불러올 때 한번에 몇개의 정수를 불러올 지를 뜻한다. 여기서는 2**10 이므로 한번 불러올 때마다 1024개의 정수를 불러온다.
    CHUNK = 1000
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 48000
    RECORD_SECONDS = 3
    WAVE_OUTPUT_FILENAME = 'audio_stt_tts/user_says/say.wav'

    p=pyaudio.PyAudio()

    stream=p.open(format=FORMAT,channels=1,rate=RATE,input=True, output=True,
            frames_per_buffer=CHUNK,input_device_index=2)

    print("*으아아ㅏ 녹음한드아ㅏㅏㅏㅏ!")
    sys.stdout.write('\a')
    sys.stdout.flush()

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    #np.frombuffer로 byte 자료형을 int로 바꿔주자
        data = stream.read(CHUNK,exception_on_overflow = False)
        frames.append(data)
    print("*끄-읕 데헷")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
