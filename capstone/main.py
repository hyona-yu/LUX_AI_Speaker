from emotion2react import *
from tts_stt import *
from socket_server import *
from thread_jh import *
##헤이 럭스 ###
run_wav('./audio_stt_tts/first_lux.wav')

go_thread() # therad_jh 가셔서 wav파일좀 만들어주세연

txt = STT('audio_stt_tts/user_says/say.wav')# , 24000) 
# 
#          #
#return txt#
####   ## ####

client = client_server() #서버 통신 class
emo2rea = emotion_to_ans() # 문장 감정에 대한 react class 
emotion, percent = client.client_server(txt).split(' ')

emo2rea.get_method(emotion)

