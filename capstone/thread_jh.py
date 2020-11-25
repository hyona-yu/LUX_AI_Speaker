import threading
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import wave
import time
import sys
import queue
global bf_data
global sample
import six
##이거슨 스레드이다. 나중에 음성 받을 때 쓸 아이이다. 아직 tts함수는 불러오지 않았다.
class isLUX():
    def __init__(self):
        self.lock = threading.Lock()
        self.lockedValue = False

    def changeStatus(self):
        self.lock.acquire()
        try:
            self.lockedValue = not(self.lockedValue)
        finally:
            self.lock.release()

class bf_data():
    def __init__(self):
        self.lock = threading.Lock()
        self.lockedValue = b'\\\x00'

    def inputBuffer(self, value):
        self.lock.acquire()
        try:
            self.lockedValue = value
        finally:
            self.lock.release()

class sample():
    def __init__(self):
        self.lock = threading.Lock()
        self.lockedValue = []
    def inputList(self, value):
        self.lock.acquire()
        try:
            self.lockedValue = value
        finally:
            self.lock.release()


isLUX = isLUX()
bf_data = bf_data()
sample = sample()

def recording_aftLUX():
    global bf_data

        #CHUNK는 음성데이터를 불러올 때 한번에 몇개의 정수를 불러올 지를 뜻한다. 여기서는 2**10 이므로 한번 불러올 때마다 1024개의 정수를 불러온다.
    CHUNK = 1
    FORMAT = pyaudio.paInt16
    RATE = 16000

        #pyaudio 열기
    p=pyaudio.PyAudio()
    stream=p.open(format=FORMAT,channels=1,rate=RATE,input=True,
                  frames_per_buffer=CHUNK,input_device_index=0)


    print("recording\n")
    while True:
        if isLUX.lockedValue == True:
            print('댜...이루었다......')
            break
        bf_data.inputBuffer(stream.read(CHUNK,exception_on_overflow = False))


    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open('say_something.wav', 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(np.array(sample)))#(b''.join(six.int2byte(sample)))
    wf.close()

def queueing_aftLUX():
    max_size = 64000
    q = queue.Queue(max_size)
    # Queue 초기화
    for i in range(1,max_size):
        q.put(0)

    global sample
    global bf_data
    global isLUX

    print("queueing Start")

    while True:
        if isLUX.lockedValue == True:
            print('fin?')
            break
        data = int(np.frombuffer(bf_data.lockedValue, dtype = np.int16))
        if q.qsize() == max_size:
            isLUX.lockedValue = True
            break
            #q.get()
        q.put(data)
        sample = (q.queue)

t1 = threading.Thread(target = recording_aftLUX)
t2 = threading.Thread(target = queueing_aftLUX)
t1.start()
t2.start()

mainThread = threading.currentThread()
for thread in threading.enumerate():
    # Main Thread를 제외한 모든 Thread들이
    # 카운팅을 완료하고 끝날 때 까지 기다린다.
    if thread is not mainThread:
        thread.join()

print('sample:', np.array(sample).tobytes())
#print('buffer:', bf_data)
