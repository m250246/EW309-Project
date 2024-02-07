import pwmio
import board
import time
import digitalio
import usb_cdc
import busio
import adafruit_bno055

class MotorController:
    def __init__(self, tilt, pan, downT, upT, leftP, rightP, sda, scl):
        # Initialize PWM for pitch/yaw motor
        self.pc = usb_cdc.data
        self.i2c = busio.I2C(scl, sda)
        self.sensor = adafruit_bno055.BNO055_I2C(self.i2c)
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
        self.pc.write(bytes('hello\n','utf-8'))

        # Initialize last_read_time to store the time of the last read_data() call
        self.last_read_time = time.time()

    def down(self, speed = 0.8, MAX = (2**16) -1):
        # Set motor direction for pitch up
        self.upT.value   = True
        self.downT.value = False
        # Set pitch motor speed
        self.tilt.duty_cycle = int(speed * MAX)

    def up(self, speed = 0.4, MAX = (2**16) -1):
        # Set motor direction for pitch down
        self.upT.value   = False
        self.downT.value = True
        # Set pitch motor speed
        self.tilt.duty_cycle = int(speed * MAX)

    def right(self, speed = 0.5, MAX = (2**16) -1):
        # Set motor direction for yaw right
        self.rightP.value   = True
        self.leftP.value    = False
        # Set yaw motor speed
        self.pan.duty_cycle = int(speed * MAX)

    def left(self, speed = 0.5, MAX = (2**16) -1):
        # Set motor direction for yaw up
        self.rightP.value   = False
        self.leftP.value    = True

        # Set yaw motor speed
        self.pan.duty_cycle = int(speed * MAX)

    def stop(self):
        # Stop the motor

        self.tilt.duty_cycle = 0
        self.pan.duty_cycle   = 0

    def read_angles(self):
        self.rollA, self.tiltA, self.panA = self.sensor.magnetic
        # Print the data
        print("Pan: {:.2f} degrees".format(self.tiltA))
        print("Tilt: {:.2f} degrees".format(self.panA))

    def read_rates(self):
        self.roll_rate, self.tilt_rate, self.pan_rate = self.sensor.gyro
        # Print the data
        print("Pan Rate: {:.2f} deg/s".format(self.pan_rate))
        print("Tilt Rate: {:.2f} deg/s\n".format(self.tilt_rate))

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
            else:
                self.stop()
        else:
            self.stop()



motor = MotorController(board.GP8, board.GP11, board.GP10, board.GP9, board.GP12, board.GP13, board.GP6, board.GP7)


while True:
    motor.key_commands()

    # Check if 5 seconds have passed since the last read_data() call
    current_time = time.time()
    if current_time - motor.last_read_time >= 3:
        motor.read_angles()
        motor.read_rates()
        motor.last_read_time = current_time

    time.sleep(0.01)

