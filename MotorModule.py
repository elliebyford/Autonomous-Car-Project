"This module is used to control the motors for the Autonomous Car"
import gopigo3
from time import sleep
from easygopigo3 import EasyGoPiGo3

gpg = gopigo3.GoPiGo3()
GPG = EasyGoPiGo3()
motor_right = gpg.MOTOR_RIGHT
motor_left = gpg.MOTOR_LEFT

port = "AD1"
sensor = GPG.init_ultrasonic_sensor(port)
sensor.set_safe_distance(127)

# Used to determine the speed, turning and timing
def direction(speed=0.5, turn=0, t=2):
    speed *= 100
    turn *= 70
    left_speed = speed + turn
    right_speed = speed - turn
    if left_speed > 100:
        left_speed = 100
    elif left_speed < -100:
        left_speed = -100
    if right_speed > 100:
        right_speed = 100
    elif right_speed < -100:
        right_speed = -100

    gpg.set_motor_power(motor_right, right_speed)
    gpg.set_motor_power(motor_left, left_speed)
    sleep(t)


def forward(speed=50):
    gpg.set_motor_power(motor_right + motor_left, speed)

def backwards(speed=50):
    gpg.set_motor_power(motor_right + motor_left, -speed)

def right_turn(speed=50):
    gpg.set_motor_power(motor_left, speed)
    gpg.set_motor_power(motor_right, 0)

def left_turn(speed=50):
    gpg.set_motor_power(motor_right, speed)
    gpg.set_motor_power(motor_left, 0)

def stop(t=0):
    gpg.set_motor_power(motor_left + motor_right, 0)
    sleep(t)

# main is used for isolation testing of the car's motors
def main():
    
    stop(2)

if __name__ == '__main__':
    while True:
        #forward()
        main()









