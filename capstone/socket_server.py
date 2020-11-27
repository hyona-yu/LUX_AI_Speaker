from socket import *
from select import *
import sys
class client_server:
	def __init__(self):
		self.add = ('34.64.253.197', 5000)
		self.client = socket(AF_INET, SOCK_STREAM)
		try  :
			self.client.connect(self.add)
		except: print('bb')
	def client_server(self,txt):
		
		try  :
			
			self.client.send(txt.encode())
			data = self.client.recv(5000)
			print(data.decode())
			return data.decode()
		except:
			print('no')

## 서버 클래스 사용 예시. 텍스트 넣어서 보내면 emotion(0:화남 1:슬픔 2:중립 3:행복), percentage 반환.
## 헤이럭스 할때 갖다 쓰세염		
if __name__ == '__main__':
	client = client_server()
	emotion, percent = client.client_server('죽기 딱 좋은 날씨로군').split(' ')
	client.client_server('그렇지 아니한가.')
	client.client_server('서버는 이걸로 완성')
	
	
