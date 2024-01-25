import pwmio
import board
import time
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

pitchM  = pwmio.PWMOut(board.GP8, frequency = 1000, duty_cycle = 25000)
pitchD  = digitalio.DigitalInOut(board.GP9)
pitchD.direction = digitalio.Direction.OUTPUT
pitchU  = digitalio.DigitalInOut(board.GP10)
pitchU.direction = digitalio.Direction.OUTPUT

yawM  = pwmio.PWMOut(board.GP11, frequency = 1000, duty_cycle = 25000)
yawL = digitalio.DigitalInOut(board.GP12)
yawL.direction = digitalio.Direction.OUTPUT
yawR = digitalio.DigitalInOut(board.GP13)
yawR.direction = digitalio.Direction.OUTPUT

k=Keyboard(usb_hid.devices)
print('\n\n\n')
k.press(Keycode., Keycode.X)
# DOWN
#    pitchD.value = True
#    pitchU.value = False
#    print('down')
#    time.sleep(1)

# UP
#    pitchD.value = False
#    pitchU.value = True
#    print('up')
#    time.sleep(1)

# LEFT
#    yawL.value = True
#    yawR.value = False
#    print('left')
#    time.sleep(1)

# RIGHT
#    yawL.value = False
#    yawR.value = True
#    print('right')
#    time.sleep(1)
