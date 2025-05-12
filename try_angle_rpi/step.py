import RPi.GPIO as GPIO
import time
from threading import Thread

class Step():
    def __init__(self):
        self.thread = None
        GPIO.setmode(GPIO.BCM)
        self.StepPins1 = [14,15,18,23]
        self.StepPins2 = [17,27,22,10]
        self.StepPins3 = [5,6,13,19]
        self.dir = 0 # 0,(center),1(left),2(right),3(up),4(down),5(front),6(back)
        self.arrow = {'center':0, 'left':1, 'right':2, 'up':3, 'down':4, 'front':5, 'back':6}
        self.initCnt = [0,0] # 얼만큼 움직였는지 저장하는 변수 (초기화할때 사용)
        self.initMode = False
        for pin in self.StepPins1:
            GPIO.setup(pin,GPIO.OUT)
            GPIO.output(pin, False)
        for pin in self.StepPins2:
            GPIO.setup(pin,GPIO.OUT)
            GPIO.output(pin, False)
        for pin in self.StepPins3:
            GPIO.setup(pin,GPIO.OUT)
            GPIO.output(pin, False)

        self.StepCounter = 0

        self.StepCount = 4
        self.Seq1 = [[0,0,0,1],
            [0,0,1,0],
            [0,1,0,0],
            [1,0,0,0]]

        self.Seq2 = [[1,0,0,0],
            [0,1,0,0],
            [0,0,1,0],
            [0,0,0,1]]

        self.Seq0 = [[0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0]]

    def run(self):
        # 모터 제어 쓰레드 생성
        if self.thread is None : # 스레드가 없다면
            self.thread = Thread(target=self.update) # 스레드 생성
            self.thread.daemon = True
            self.thread.start() # 스레드 시작

    def update(self):
        try:
            while True:
                for pin in range(0,4):
                    xpin = self.StepPins1[pin]
                    ypin = self.StepPins2[pin]
                    zpin = self.StepPins3[pin]
                    # left
                    if self.dir == 1:
                        self.initCnt[1] -= 1
                        if self.Seq1[self.StepCounter][pin]!=0:
                            GPIO.output(xpin, True)
                        else:
                            GPIO.output(xpin, False)
                    # down        
                    elif self.dir == 2:
                        self.initCnt[1] += 1
                        if self.Seq2[self.StepCounter][pin]!=0:
                            GPIO.output(xpin, True)
                        else:
                            GPIO.output(xpin, False)
                    # up
                    elif self.dir == 3 or self.dir == 5:
                        self.initCnt[0] += 1
                        if self.Seq1[self.StepCounter][pin]!=0:
                            GPIO.output(ypin, True)
                        else:
                            GPIO.output(ypin, False)
                        if self.Seq2[self.StepCounter][pin]!=0:
                            GPIO.output(zpin, True)
                        else:
                            GPIO.output(zpin, False)
                    # down
                    elif self.dir == 4 or self.dir == 6:
                        self.initCnt[0] -= 1
                        if self.Seq2[self.StepCounter][pin]!=0:
                            GPIO.output(ypin, True)
                        else:
                            GPIO.output(ypin, False)
                        if self.Seq1[self.StepCounter][pin]!=0:
                            GPIO.output(zpin, True)
                        else:
                            GPIO.output(zpin, False)
                    # center, 측정범위 벗어나면 정지        
                    else:
                        if self.Seq0[self.StepCounter][pin]!=0:
                            GPIO.output(xpin, True)
                        else:
                            GPIO.output(xpin, False)
                self.StepCounter += 1

                if (self.StepCounter == self.StepCount):
                    self.StepCounter = 0
                if (self.StepCounter < 0):
                    self.StepCounter = self.StepCount

                time.sleep(0.05)
        except KeyboardInterrupt:
            GPIO.cleanup()

    def change(self, dir):
        try:
            self.dir = self.arrow[dir]
        except:
            self.dir = -1
            pass
    
    def initMotor(self):
        pass


                    

if __name__ == "__main__":
    st = Step()
    st.run()