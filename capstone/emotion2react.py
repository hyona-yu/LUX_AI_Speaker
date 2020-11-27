import pygame
import random
import os
import pandas as pd
import pyaudio
import wave
### 참고로 pygame 버전 1.9.x 해야함 
def run_wav(path):
	chunk = 1024
	with wave.open(path, 'rb') as f:
		p = pyaudio.PyAudio()
		stream = p.open(format = p.get_format_from_width(f.getsampwidth()),channels = f.getnchannels(), rate = f.getframerate(), output= True)
		data = f.readframes(chunk)
		while data:
			stream.write(data)
			data = f.readframes(chunk)
		stream.stop_stream()
		stream.close()
		p.terminate()
	

	
class emotion_to_ans():
    def __init__(self):
        self.emotion = 0
  	#methods = {'mp3':0, 'sentence':1, 'words':2 }# 감성노래, 힘내요 대답!, 감성글

    def get_method(self, emotion):
        self.emotion = int(emotion)
        run_wav('audio_stt_tts/'+str(self.emotion)+'_emotion_status.wav')
        if self.emotion <2:
        	self.get_method = random.randrange(0,2) # mp3 불러올건지 sentence 불러올건지 감성글 불러올건지
        else:
        	self.get_method = random.randrange(0,3)
        	
        self.get_method = 0

        if self.get_method ==0:
            self.method_mp3(self.emotion)

        elif self.get_method ==1:
            self.method_sen(self.emotion)

        elif self.get_method ==2:
            self.method_words(self.emotion)

#https://m.blog.naver.com/iamhyel/221990422616 무료 음원 다운
    def method_mp3(self, emotion):
    	run_wav('audio_stt_tts/'+str(0)+'_emotion2react.wav')
    	mp3_path = 'mp3_folder/'
    	mp3s = os.listdir(mp3_path)
    	emotion_mp3 = []
    	for p in mp3s:
    		if p.split('_')[0] == str(emotion):
    			emotion_mp3.append(p)
    	idx = random.randrange(0, len(emotion_mp3))
    	freq = 44100    # sampling rate, 44100(CD), 16000(Naver TTS), 24000(google TTS)
    	bitsize = -16   # signed 16 bit. support 8,-8,16,-16
    	channels = 1    # 1 is mono, 2 is stere
    	buffer = 4096   # number of samples (experiment to get right sound)
    	print(os.path.join(mp3_path , emotion_mp3[idx]))
    	pygame.mixer.init(freq, bitsize, channels, buffer=4096)
    	pygame.mixer.music.load(os.path.join(mp3_path , emotion_mp3[idx]))
    	pygame.mixer.music.play()
    	clock = pygame.time.Clock()
    	while pygame.mixer.music.get_busy():
    		clock.tick(10)
    		pygame.mixer.quit()
        


    def method_sen(self, emotion, sen_path = './audio_stt_tts/emotion_sen/'):
        run_wav('audio_stt_tts/'+str(2)+'_emotion2react.wav')
        sen = os.listdir(sen_path)
        emotion_sen = []
        for s in sen:
        	if int(s.split('_')[0]) == emotion:
        		emotion_sen.append(sen_path + s)
        	
        idx = random.randrange(0, len(emotion_sen))
        
        run_wav(emotion_sen[idx])

        #return emotion_sen[idx]

    def method_words(self, emotion, gamsung_path ='audio_stt_tts/gamsung_sen/'):
        run_wav('audio_stt_tts/'+str(1)+'_emotion2react.wav')
        sen = os.listdir(gamsung_path)
        gamsung_sen = []
        for s in sen:
        	if int(s.split('_')[0]) == emotion:
        		gamsung_sen.append(gamsung_path + s)
        		
        idx = random.randrange(0, len(gamsung_sen))
        run_wav(gamsung_sen[idx])

if __name__ =='__main__':
    ans = emotion_to_ans()
    ans.get_method(1)
