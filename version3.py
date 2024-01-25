import pwmio
import board
import time
import digitalio
import usb_hid
#from adafruit_hid.keyboard import Keyboard
#from adafruit_hid.keyboard import Keycode
import usb_cdc
#chatGPT
#question: create a classin circut python that moves a L298 H-Bridge motor and have key imputs



class MotorController:
    def __init__(self, tilt, pan, downT, upT, leftP, rightP):
        # Initialize PWM for pitch/yaw motor
        self.pc = usb_cdc.data
        self.tilt = pwmio.PWMOut(tilt, frequency = 600, duty_cycle = 0)
        self.pan   = pwmio.PWMOut(pan, frequency = 600, duty_cycle = 0)

        # Initialize digital output for GP pins

        self.downT = digitalio.DigitalInOut(downT)
        self.upT   = digitalio.DigitalInOut(upT)
        self.leftP = digitalio.DigitalInOut(leftP)
        self.rightP= digitalio.DigitalInOut(rightP)

        # Direction Signal
        self.downT.direction = digitalio.Direction.OUTPUT
        self.upT.direction = digitalio.Direction.OUTPUT
        self.leftP.direction = digitalio.Direction.OUTPUT
        self.rightP.direction = digitalio.Direction.OUTPUT

        #self.keyboard = Keyboard(usb_hid.devices)
        self.pc.write(bytes('hello','utf-8'))


    def up(self, speed = 0.5, MAX = (2**16) -1):
        # Set motor direction for pitch up
        self.upT.value   = True
        self.downT.value = False

        # Set pitch motor speed
        self.tilt.duty_cycle = int(speed * MAX)


    def down(self, speed = 0.4, MAX = (2**16) -1):
        # Set motor direction for pitch down
        self.upT.value   = False
        self.downT.value = True

        # Set pitch motor speed
        self.tilt.duty_cycle = int(speed * MAX)


    def right(self, speed = 0.2, MAX = (2**16) -1):
        # Set motor direction for yaw right
        self.rightP.value   = True
        self.leftP.value    = False

        # Set yaw motor speed
        self.pan.duty_cycle = int(speed * MAX)


    def left(self, speed = 0.2, MAX = (2**16) -1):
        # Set motor direction for yaw up
        self.rightP.value   = False
        self.leftP.value    = True

        # Set yaw motor speed
        self.pan.duty_cycle = int(speed * MAX)

    def stop(self):
        # Stop the motor

        self.tilt.duty_cycle = 0
        self.pan.duty_cycle   = 0

    def key_commands(self):
        # Check if keys are being pressed
        if self.pc.in_waiting >0:
            inputs = self.pc.read(self.pc.in_waiting).strip().decode()
            print('Key Pressed:  ', inputs)
            if inputs =='w':
                print('up')
                self.up()
            elif inputs=='s':
                print('down')
                self.down()
            elif inputs=='a':
                print('left')
                self.left()
            elif inputs=='d':
                print('right')
                self.right()
            else:
                self.stop()



motor = MotorController(board.GP8, board.GP11, board.GP10, board.GP9, board.GP12, board.GP13)


while True:
    motor.key_commands()
    time.sleep(0.01)

