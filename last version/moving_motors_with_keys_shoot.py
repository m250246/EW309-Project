from MotorController import Motor
import board
import time
import usb_cdc
import math



motor = Motor(board.GP8, board.GP11, board.GP10, board.GP9, board.GP12, board.GP13, board.GP6, board.GP7, board.GP15, board.GP14)
print('\n\n\n')
motor.shots = 1
motor.printTime = 1
while True:
    motor.read_keys()
    motor.print_data()
    time.sleep(0.01)
