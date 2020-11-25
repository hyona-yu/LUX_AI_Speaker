#### TTS ####
#pip3 install --upgrade google-cloud-texttospeech
#extract GOOGLE_APPLICATION_CREDENTIALS = "impactful-post-296307-1929e49da366.json"


#### SST ####
# rate 16000Hz 
import io
import os
from google.cloud import speech
from google.cloud import texttospeech

def TTS(text, file_path):
	client = texttospeech.TextToSpeechClient()
	syn_input = texttospeech.SynthesisInput(text = text)
	voice = texttospeech.VoiceSelectionParams(language_code = "ko-KR")
	audio = texttospeech.AudioConfig(audio_encoding = texttospeech.AudioEncoding.LINEAR16)
	response = client.synthesize_speech(input = syn_input, voice = voice, audio_config = audio)
	with open(file_path, 'wb') as out:
		out.write(response.audio_content)

def STT(file_path, rate = 16000):
	client = speech.SpeechClient()
	file_name = os.path.join(os.path.dirname(__file__), file_path)
	with io.open(file_name , 'rb') as audio_:
		content = audio_.read()
		audio= speech.RecognitionAudio(content = content)
	config = speech.RecognitionConfig(encoding = speech.RecognitionConfig.AudioEncoding.LINEAR16, sample_rate_hertz=rate, language_code = "ko-KR")   
	response = client.recognize(config = config, audio = audio)
	for result in response.results:
		print(result.alternatives[0].transcript)
	

if __name__ == '__main__':
	STT('./audio_stt_tts/3_emotion_status.wav', 24000)
	#TTS('화가 나셨군요', './audio_stt_tts/0_emotion_status.wav')

