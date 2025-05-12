from socket import *
from threading import Thread
from step import * # 스텝 모터


class Motor():
    def __init__(self):
        self.arrow = None
        self.thread = None
        self.sock = None
        self.client = None
        self.isRunning = False
        self.cnt = 0

    def run(self): 
        # 데이터를 받을 쓰레드 생성
        if self.thread is None : # 스레드가 없다면
            self.thread = Thread(target=self.update) # 스레드 생성
            self.thread.daemon = True
            self.thread.start() # 스레드 시작

    def update(self):
        self.isRunning = True
        st = Step() # 스텝 모터 객체 생성성
        st.run() # 스텝 모터 시작
        while True:
            try:
                self.cnt = 0
                self.sock = None
                self.sock = socket(AF_INET, SOCK_STREAM)
                self.sock.bind(('192.168.80.73', 8888)) # 어플과 통신, 성공하면 모터 연결
                self.sock.listen(1)
                print('accept motor...')
                if self.sock is None:
                    break
                self.client, self.addr = self.sock.accept()
                print('connect motor!!')
                while True:
                    try:
                        data = self.client.recv(10)
                    except:
                        break
                    else:
                        if not data:
                            break
                        dir = data.decode()
                        print(f'dir : {dir}')
                        st.change(dir) # 모터 방향 변경

                        print(f'st : {st.dir}')
                        if dir == 'good': # 구도가 좋으면 카운트 시작 (3초 이상 유지시 촬영 <- 어플에서 처리)
                            self.cnt += 1
                        else:
                            self.cnt = 0
                        self.client.send(f'{self.cnt}'.encode())

            except Exception as e:
                print('Error Motor:', e)
                if self.is_socket_open(self.sock) and self.sock is not None:
                    self.sock.close()
            finally:
                if self.is_socket_open(self.sock) and self.sock is not None:
                    self.stop()
                    self.sock.close()
                    print('motor 소켓 닫음')

    def stop(self):
        if self.is_socket_open(self.client) and self.client is not None:
            self.client.close()
            self.client = None
        if self.is_socket_open(self.sock) and self.sock is not None:
            self.sock.close()
            self.sock = None
            print('motor 소켓 강제 종료')

    def is_socket_open(self, sock):
        if sock is None:
            return False
        try:
            # 소켓의 파일 디스크립터를 확인
            fileno = sock.fileno()
            return fileno != -1
        except error:
            # 소켓 에러가 발생하면 닫혀 있음을 의미
            return False
            

if __name__ == "__main__":
    motor = Motor()
    motor.run()
    while motor.isRunning:
        continue