import pygame
import random
import os
import pandas as pd
import pyaudio
import wave
#이거슨 감정받은 후에 매핑 함수다. ㅔpath 잘 바꿔라. 아직 tts로 말하는거 안넣었다. 
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
  #methods = {'mp3':0, 'sentence':1, 'words':2 }# 감성노래, 감성글, 힘내요 대답!
        sentence_path = ''

    def get_method(self, emotion):
        self.emotion = emotion
        run_wav('audio_stt_tts/'+str(self.emotion)+'_emotion_status.wav')
        self.get_method = random.randrange(0,3) # mp3 불러올건지 sentence 불러올건지 감성글 불러올건지
  #words = ['괜찮아요', '힘내요','내일은 다시 웃어봐요']
        if self.get_method ==0:
            self.method_mp3(emotion)

        elif self.get_method ==1:
            self.method_sen(emotion)

        elif self.get_method ==2:
            self.method_words(emotion)


    def method_mp3(self, emotion):
        run_wav('audio_stt_tts/'+str(0)+'_emotion2react.wav')
        mp3_path = 'C:/Users/gysk0/Desktop/capstone/mp3_folder/'
        mp3s = os.listdir(mp3_path)#['0_Winner_Winner_Funky_Chicken_Dinner.mp3', '0_Luxery.mp3']#예시파
        emotion_mp3 = []
        


    def method_sen(emotion, sen_path = 'C:/Users/gysk0/Desktop/capstone/'):
        run_wav('audio_stt_tts/'+str(1)+'_emotion2react.wav')
        sen = pd.read_csv(sen_path)
        emotion_sen =sen[sen['Label'] == emotion]
        idx = random.randrange(0, len(emotion_sen))

        return emotion_sen[idx]

    def method_words(emotion, word_path =''):
        run_wav('audio_stt_tts/'+str(2)+'_emotion2react.wav')
        word = pd.read_csv(word_path)
        word_sen = sen[sen['Emotion']== emotion]
        idx = random.randrange(0, len(word_sen))
        return word_sen[idx]

if __name__ =='__main__':
    ans = emotion_to_ans()
    ans.get_method(0)
