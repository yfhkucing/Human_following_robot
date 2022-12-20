from pyfirmata import Arduino, SERVO, util, PWM, OUTPUT
from time import sleep

pin = 4
pin2 = 7
port = '/dev/ttyACM0'
Board = Arduino(port)
Board.digital[2].mode = OUTPUT #RF
Board.digital[3].mode = OUTPUT #RB
Board.digital[5].mode = PWM #R
Board.digital[6].mode = PWM #L
Board.digital[9].mode = OUTPUT #LF
Board.digital[10].mode = OUTPUT #LB
Board.digital[pin].mode=SERVO
Board.digital[pin2].mode=SERVO

#fungsi servo
def servo1(angle):
    Board.digital[4].write(angle)
    sleep(0.015)

def servo2(angle):
    Board.digital[7].write(angle)
    sleep(0.015)

def control(direction,side,pwm) :
    if direction == "forward":
        if side == "right":
            Board.digital[5].write(pwm)
            Board.digital[2].write(1)
            Board.digital[3].write(0)
        elif side == "left":
            Board.digital[6].write(pwm)
            Board.digital[9].write(1)
            Board.digital[10].write(0)
        elif direction == "backward":
            if side == "right":
                Board.digital[5].write(pwm)
                Board.digital[3].write(1)
                Board.digital[2].write(0)
        elif side == "left":
            Board.digital[6].write(pwm)
            Board.digital[9].write(0)
            Board.digital[10].write(1)
    else :
        Board.digital[3].write(0)
        Board.digital[2].write(0)
        Board.digital[5].write(0)
        Board.digital[6].write(0)
        