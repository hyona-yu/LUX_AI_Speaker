import numpy as np
import pandas
import tensorflow_hub as hub
import tensorflow as tf
import urllib.request
import time
from keras.models import Model
from keras.layers import Dense, Lambda, Input, Dropout
from keras import optimizers
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import re
import json
#####  리눅스 최종 version  #####  
### tensorflow version: 1.15.2, tensorflow_hub version : 0.10.0 (걍 깔면 이거 됨), keras 2.3.1
### h5py version 2.10.0
class ELMO():
  def __init__(self):
    self.elmo = hub.Module("https://tfhub.dev/google/elmo/1", trainable=True)
    self.okt = Okt()
  def ELMoEmbedding(self, x):
    return self.elmo(tf.squeeze(tf.cast(x, tf.string)))
  def elmo_model(self):
    input_text = Input(shape=(1,), dtype=tf.string)
    embedding_layer = Lambda(self.ELMoEmbedding, output_shape=(1024, ))(input_text)
    hidden_layer = Dense(256, activation='relu')(embedding_layer)
    dropout = Dropout(0.5)(hidden_layer)
    output_layer = Dense(4, activation='softmax')(dropout)
    model = Model(inputs = [input_text], outputs = output_layer)
    model.load_weights('./params/real_elmo_weight.h5')
    return model

  def tokenize(self, data):
      stopwords = ['ㅋ','ㅎ','ㅠㅠ','ㅜㅜ','^^','의','을','(','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다']

      han = re.compile(r"[^ㄱ-ㅎㅏ-ㅣ가-힣 ]")
      arr = []
      for sen in data:
          sen = re.sub(han, "", sen)
          temp = self.okt.morphs(sen, stem = True)#True
          temp = [word for word in temp if not word in stopwords]
          arr.append(' '.join(temp))
      return arr

  def elmo_model_2(self):
    input_text = Input(shape=(1,), dtype=tf.string)
    embedding_layer = Lambda(self.ELMoEmbedding, output_shape=(1024, ))(input_text)
    hidden_layer = Dense(256, activation='relu')(embedding_layer)
    dropout = Dropout(0.5)(hidden_layer)
    output_layer = Dense(4, activation='softmax')(dropout)
    model = Model(inputs = [input_text], outputs = output_layer)
    model.load_weights('./params/best_t_elmo_model_onlytrain_weight.h5')

    return model

class GRU_model():
    def __init__(self):
        self.max_len = 8
        self.okt = Okt()
        self.num_words = 8709
        self.tokenizer = Tokenizer(num_words = self.num_words + 1)
        with open('./params/base_wordIndex.json') as json_file:
            word_index = json.load(json_file)
            self.tokenizer.word_index = word_index
    def base_model(self):
        model = load_model('./params/base_t_model.h5')
        return model


    def tokenize(self, single_data):
        sen = single_data
        stopwords = ['ㅋ','ㅎ','ㅠㅠ','ㅜㅜ','^^','의','을','(','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다']

        han = re.compile(r"[^ㄱ-ㅎㅏ-ㅣ가-힣 ]")

        sen = re.sub(han, "", sen)
        temp = self.okt.morphs(sen, stem = True)#True
        temp = [word for word in temp if not word in stopwords]
      #arr.append(temp)
        return temp


class predict():
    def __init__(self):
        self.gru = GRU_model()
        self.elmo = ELMO()
        self.base_model = self.gru.base_model()
        self.loaded_model = self.elmo.elmo_model()
        self.train_loaded_model = self.elmo.elmo_model_2()


    def predict_base(self, new_sentence):
        new_sen = self.gru.tokenize(new_sentence)
        encoded = self.gru.tokenizer.texts_to_sequences([new_sen])
        pad_new = pad_sequences(encoded, maxlen = self.gru.max_len)
        pred = self.base_model.predict(pad_new)
        return pred

    def predict_elmo(self, new_sentence):
        data = [new_sentence, '']
        new_sen = self.elmo.tokenize(data)
        pred = self.loaded_model.predict(np.array(new_sen))
        return pred
    def predict_train_elmo(self, new_sentence):
        data = [new_sentence, '']
        new_sen = self.elmo.tokenize(data)
        pred = self.train_loaded_model.predict(np.array(new_sen))
        return pred

    def soft_voting_ensemble(self, p1, p2, p3):
        return p1 + p2 + p3

    def predict(self, new_sentence):
        pred = self.predict_elmo(new_sentence)
        pred_base = self.predict_base(new_sentence)
        pred_train_elmo = self.predict_train_elmo(new_sentence)

        if np.max(pred[0])>=0.6:
            return np.argmax(pred[0]), np.max(pred[0])
            #print('%.2f'%(np.max(pred[0])*100) +'% 의 확률로 ',emotion_dic[np.argmax(pred[0])])
        else:
            voting_pred = self.soft_voting_ensemble(pred[0], pred_train_elmo[0], pred_base)
            return np.argmax(voting_pred[0]), np.max(voting_pred[0])*100/3
            #print('%.2f'%(np.max(voting_pred[0])*100/3) +'% 의 확률로 ',emotion_dic[np.argmax(voting_pred[0])])



if __name__ == '__main__':
    predict_class= predict()
    print(predict_class.predict('마구니가 가득가득 끼는중 '))
