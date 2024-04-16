from MotorController import Motor
import board
import time
import usb_cdc
import math


print("\n")
motor = Motor(board.GP8, board.GP11, board.GP10, board.GP9, board.GP12, board.GP13, board.GP6, board.GP7, board.GP15, board.GP14)

while True:
    motor.enter_keys()
    motor.target()
    motor.shooting()
