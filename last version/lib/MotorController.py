import pwmio
import time
import digitalio
import usb_cdc
import busio
import adafruit_bno055
import sys

class Motor:
    def __init__(self, tilt, pan, downT, upT, leftP, rightP, sda, scl, shooter, feeder):
        # Initialize PWM for pitch/yaw motor
        self.i2c = busio.I2C(scl, sda)
        self.sensor = adafruit_bno055.BNO055_I2C(self.i2c)
        self.tilt = pwmio.PWMOut(tilt, frequency = 1000, duty_cycle = 0)
        self.pan   = pwmio.PWMOut(pan, frequency = 1000, duty_cycle = 0)
        self.shoot = pwmio.PWMOut(shooter, frequency = 1000, duty_cycle = 0)
        self.feed = pwmio.PWMOut(feeder, frequency = 1000, duty_cycle = 0)

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

        #self.pc.write(bytes('arrows: \n','utf-8'))

        self.MAX = (2**16)-1
        # Initialize last_read_time to store the time of the last read_data() call
        self.initialT = time.monotonic()
        self.lastTime = 0
        self.printTime = 0.1

        self.panA = 0
        self.tiltA = 0
        self.rollA = 0
        self.roll_rate = 0
        self.tilt_rate = 0
        self.pan_rate = 0

    def down(self, speed = 1):
        # Set motor direction for pitch up
        self.upT.value   = True
        self.downT.value = False
        # Set pitch motor speed
        self.tilt.duty_cycle = int(speed * self.MAX)

    def up(self, speed = 1):
        # Set motor direction for pitch down
        self.upT.value   = False
        self.downT.value = True
        # Set pitch motor speed
        self.tilt.duty_cycle = int(speed * self.MAX)

    def right(self, speed = 1):
        # Set motor direction for yaw right
        self.rightP.value   = True
        self.leftP.value    = False
        # Set yaw motor speed
        self.pan.duty_cycle = int(speed * self.MAX)

    def left(self, speed = 1):
        # Set motor direction for yaw up
        self.rightP.value   = False
        self.leftP.value    = True
        # Set yaw motor speed
        self.pan.duty_cycle = int(speed * self.MAX)

    def stop(self):
        # Stop the motor
        # need to figure out how to BRAKE instead of rolling motion for the up
        self.tilt.duty_cycle = 0
        self.upT.value   = False
        self.downT.value = False
        self.pan.duty_cycle   = 0
        self.rightP.value   = False
        self.leftP.value    = False
        self.shoot.duty_cycle = 0
        self.feed.duty_cycle = 0

    def shooting(self):
        self.shoot.duty_cycle = int(.75*self.MAX)
        time.sleep(4)
        for i in range(5):
            self.feed.duty_cycle = int(self.MAX)
            time.sleep(.25)
            self.feed.duty_cycle = 0
            time.sleep(1)

    def data(self):
        self.panA, self.tiltA, self.rollA = self.sensor.euler
        self.roll_rate, self.tilt_rate, self.pan_rate = self.sensor.gyro
        self.tiltA = -1*self.tiltA
        if self.panA < 100:
            self.panA += 360
        self.panA -= 360

    def print_data(self):
        self.current_time = time.monotonic() - self.initialT
        if self.current_time - self.lastTime >= self.printTime:
            self.panA, self.tiltA, self.rollA = self.sensor.euler
            self.roll_rate, self.tilt_rate, self.pan_rate = self.sensor.gyro
            self.tiltA = -1*self.tiltA
            if self.panA < 100:
                self.panA += 360
            self.panA -= 360
            if self.printTime<0.1:
                print("{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f}".format(self.current_time, self.panA, self.tiltA, self.rollA, self.pan_rate, self.tilt_rate, self.roll_rate))
            else:
                print("{:.1f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f}".format(self.current_time, self.panA, self.tiltA, self.rollA, self.pan_rate, self.tilt_rate, self.roll_rate))
            self.lastTime = self.current_time

    def test_dz_data(self, setspeed):
        self.current_time = round(time.monotonic() - self.initialT,1)
        if self.current_time - self.lastTime >= self.printTime:
            self.panA, self.tiltA, self.rollA = self.sensor.euler
            self.roll_rate, self.tilt_rate, self.pan_rate = self.sensor.gyro
            self.tiltA = -1*self.tiltA
            if self.panA < 100:
                self.panA += 360
            self.panA -=270
            if self.printTime<0.1:
                print("{:.2f},{:.2f},{:.2f},{:.2f}".format(self.current_time, self.pan_rate, self.tilt_rate,setspeed))
            else:
                print("{:.1f},{:.2f},{:.2f},{:.2f}".format(self.current_time, self.pan_rate, self.tilt_rate,setspeed))
            self.lastTime = self.current_time

    def read_keys(self):
        # Check if keys are being pressed
        #self.pc.flush()
        if self.pc.in_waiting > 0:
            inputs = self.pc.read(1).strip()#.decode()
            print(inputs)
            if inputs ==b'w':
                self.up()
            elif inputs==b's':
                self.down()
            elif inputs==b'a':
                self.left()
            elif inputs==b'd':
                self.right()
            elif inputs==b'q':
                sys.exit()
            elif inputs==b'':
                self.shooting()
            else:
                self.stop()
        else:
            self.stop()

