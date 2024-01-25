# Write your code here :-)
import adafruit_bno055
import supervisor
from motor_driver_L298 import motor_L298
import usb_cdc

ser_data = usb_cdc.data
ser_console = usb_cdc.console

pitch = motor_L298(board.GP9, board.GP10, board.GP8)
yaw = motor_L298(board.GP12, board.GP13, board.GP11)
l2c = busio.I2C(board.GP7, board.GP6)
