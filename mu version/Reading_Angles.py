import pwmio
import board
import time
import digitalio
import usb_cdc
import busio
import adafruit_bno055

pc = usb_cdc.data
i2c = busio.I2C(board.GP7, board.GP6)
sensor = adafruit_bno055.BNO055_I2C(i2c)
while True:
    heading, roll, pitch = sensor.magnetic
    print("Y: {:.2f} degrees".format(heading))
    print("X: {:.2f} degrees".format(roll))
    print("Z: {:.2f} degrees\n\n".format(pitch))
    time.sleep(1)

