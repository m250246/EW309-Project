import pwmio
import board
import time
import digitalio
import usb_cdc
import busio
import adafruit_bno055
import sys

class MotorController:
    def __init__(self, tilt, pan, downT, upT, leftP, rightP, sda, scl):
        # Initialize PWM for pitch/yaw motor
        self.pc = usb_cdc.data
        self.i2c = busio.I2C(scl, sda)
        self.sensor = adafruit_bno055.BNO055_I2C(self.i2c)
        self.tilt = pwmio.PWMOut(tilt, frequency = 1000, duty_cycle = 0)
        self.pan   = pwmio.PWMOut(pan, frequency = 1000, duty_cycle = 0)
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
        self.pc.write(bytes('hello\n','utf-8'))
        self.MAX = (2**16)-1
        # Initialize last_read_time to store the time of the last read_data() call
        self.initialT = time.monotonic()


    def down(self, speed = 0.7):
        # Set motor direction for pitch up
        self.upT.value   = True
        self.downT.value = False
        # Set pitch motor speed
        self.tilt.duty_cycle = int(speed * self.MAX)
        time.sleep(.1)

    def up(self, speed = 0.4):
        # Set motor direction for pitch down
        self.upT.value   = False
        self.downT.value = True
        # Set pitch motor speed
        self.tilt.duty_cycle = int(speed * self.MAX)
        time.sleep(.1)

    def right(self, speed = 0.7):
        # Set motor direction for yaw right
        self.rightP.value   = True
        self.leftP.value    = False
        # Set yaw motor speed
        self.pan.duty_cycle = int(speed * self.MAX)
        time.sleep(.1)

    def left(self, speed = 0.7):
        # Set motor direction for yaw up
        self.rightP.value   = False
        self.leftP.value    = True
        # Set yaw motor speed
        self.pan.duty_cycle = int(speed * self.MAX)
        time.sleep(.1)

    def stop(self):
        # Stop the motor

        self.tilt.duty_cycle = 0
        self.pan.duty_cycle   = 0

        time.sleep(.1)

    def print_data(self):
        self.rollA, self.panA, self.tiltA = self.sensor.magnetic
        self.roll_rate, self.tilt_rate, self.pan_rate = self.sensor.gyro
        elapsed_time = time.monotonic() - self.initialT
        print("{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f}".format(elapsed_time, self.panA, self.tiltA, self.rollA, self.pan_rate, self.tilt_rate, self.roll_rate))

    def key_commands(self):
        # Check if keys are being pressed
        if self.pc.in_waiting > 0:
            inputs = self.pc.read().strip().decode()
            if inputs =='w':
                self.up()
            elif inputs=='s':
                self.down()
            elif inputs=='a':
                self.left()
            elif inputs=='d':
                self.right()
            elif inputs=='q':
                sys.exit()
            else:
                self.stop()
        else:
            self.stop()


motor = MotorController(board.GP8, board.GP11, board.GP10, board.GP9, board.GP12, board.GP13, board.GP6, board.GP7)
print('\n\n\n')

for i in range(2):
    motor.right()
    time.sleep(.1)
    motor.left()
    time.sleep(.1)
    motor.stop()
    time.sleep(1)
time.sleep(2)

print("\ntime, pan angle, tilt angle, pan rate, tilt rate")
# Loop for 4 iterations

#for i in range(4):
#    start_time = time.monotonic()
#    while time.monotonic() - start_time <= 2:
#        motor.stop()
#        motor.print_data()

#    start_time=time.monotonic()
#    while time.monotonic() - start_time <= 1:
#        motor.print_data()
#        motor.right()

#    start_time = time.monotonic()
#    while time.monotonic() - start_time <= 2:
#        motor.stop()
#        motor.print_data()

#    start_time = time.monotonic()
#    while time.monotonic() - start_time <= 1:
#        motor.print_data()
#        motor.left()
#motor.stop()
for i in range(5):
    start_time = time.monotonic()
    while time.monotonic() - start_time <= 2:
        motor.stop()
        motor.print_data()

    start_time=time.monotonic()
    while time.monotonic() - start_time <= 2:
        motor.print_data()
        motor.left()

    start_time = time.monotonic()
    while time.monotonic() - start_time <= 2:
        motor.stop()
        motor.print_data()

    start_time = time.monotonic()
    while time.monotonic() - start_time <= 2:
        motor.print_data()
        motor.right()
