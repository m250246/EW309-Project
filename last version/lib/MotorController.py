import pwmio
import time
import digitalio
import usb_cdc
import busio
import adafruit_bno055
import sys
import math

class Motor:
    def __init__(self, tilt, pan, downT, upT, leftP, rightP, sda, scl, shooter, feeder):
        # Initialize PWM for pitch/yaw motor
        self.pc = usb_cdc.data
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

        self.tilt_kp = 1.4
        self.tilt_ki = 0.2
        self.tilt_kd = 0
        self.yaw_kp = 1.8
        self.yaw_ki = 0.2
        self.yaw_kd = 0.01

        self.dz_up= 0.13
        self.dz_down = 0.34
        self.dz_yaw = 0.17

        self.yaw_errP = 0
        self.tilt_errP = 0
        self.yaw_errI = 0
        self.tilt_errI = 0
        self.yaw_errD = 0
        self.tilt_errD = 0


        self.des_tilt = 0
        self.des_yaw = 0
        self.shots = 0

        self.pc.reset_input_buffer()
        self.pc.reset_output_buffer()

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
        if self.shots == 0:
            pass
        else:
            for i in range(self.shots):
                self.shoot.duty_cycle = int(.75*self.MAX)
                time.sleep(4)
                self.feed.duty_cycle = int(self.MAX)
                time.sleep(.2)
                self.feed.duty_cycle = 0
                time.sleep(.5)
        self.shoot.duty_cycle = 0

    def data(self):
        self.panA, self.tiltA, self.rollA = self.sensor.euler
        self.roll_rate, self.tilt_rate, self.pan_rate = self.sensor.gyro
        self.tiltA = -1*self.tiltA
        if self.panA < 100:
            self.panA += 360
        self.panA -= 360
        self.t_elapsed = time.monotonic() - self.initialT # measure time since start of experiment
        self.tiltArad = self.tiltA*(math.pi/180)
        self.tilt_errP = self.des_tilt - self.tiltArad
        self.panArad = self.panA*(math.pi/180)
        self.yaw_errP = self.des_yaw - self.panArad

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

    def enter_keys(self):
        # Check info entered from TeraTerm
        self.pc.reset_input_buffer()
        self.pc.reset_output_buffer()
        time.sleep(2)
        self.pc.write(b"Yaw Angle:\n")
        yaw = self.pc.readline().strip().decode()
        self.des_yaw = int(yaw)*math.pi/180
        self.pc.write(b"Tilt Angle:\n")
        tilt = self.pc.readline().strip().decode()
        self.des_tilt = int(tilt)*math.pi/180
        self.pc.write(b"Shots:\n")
        shotnum = self.pc.readline().strip().decode()
        self.shots = int(shotnum)
        #self.pc.write(b"q\n")

    def target(self):
        self.data()
        while abs(self.tilt_errP*180/math.pi) > 0.1 or abs(self.yaw_errP*180/math.pi)>0.1:
            print(abs(self.tilt_errP*180/math.pi), abs(self.yaw_errP)*180/math.pi)
            self.data()
            self.tilt_controller()
            self.yaw_controller()

        self.stop()


    def tilt_controller(self):
        #self.data()
        #self.tiltArad = self.tiltA*(math.pi/180)
        #self.t_elapsed = time.monotonic() - self.initialT # measure time since start of experiment
        #self.tilt_errP = self.des_tilt - self.tiltArad
        self.tilt_errD = 0 - self.tilt_rate
        self.tilt_outspd = self.tilt_kp*self.tilt_errP + self.tilt_ki*self.tilt_errI + self.tilt_kd*self.tilt_errD  # PI_Lead controller

        if self.tilt_outspd > 0:
            self.tilt_outspd += self.dz_up
        if self.tilt_outspd < 0:
            self.tilt_outspd -= self.dz_down

        if self.tilt_outspd > 1: # make sure motor input is between [-1,1]
            self.tilt_outspd = 1
        if self.tilt_outspd < -1:
            self.tilt_outspd = -1

        if abs(self.tilt_errP * (180 / math.pi)) <= 0.1:
            self.tilt_outspd = 0.0008

        #print(self.tilt_outspd, self.tilt_errP*(180/math.pi), self.tiltA)

        if self.tilt_outspd < 0:
            self.down(speed=-1*self.tilt_outspd)
        else:
            self.up(speed=self.tilt_outspd)

        self.tilt_errI = self.tilt_errP*(self.t_elapsed-self.lastTime)
        time.sleep(0.01)
        self.lastTime = self.t_elapsed

    def yaw_controller(self):
        #self.data()
        #self.panArad = self.panA*(math.pi/180)
        #self.t_elapsed = time.monotonic() - self.initialT # measure time since start of experiment
        #self.yaw_errP = self.des_yaw - self.panArad
        self.yaw_errD = 0 - self.pan_rate
        self.yaw_outspd = self.yaw_kp*self.yaw_errP + self.yaw_ki*self.yaw_errI + self.yaw_kd*self.yaw_errD  # PI_Lead controller
        if self.yaw_outspd > 0:
            self.yaw_outspd += self.dz_yaw
        if self.yaw_outspd < 0:
            self.yaw_outspd -= self.dz_yaw

        if self.yaw_outspd > 1: # make sure motor input is between [-1,1]
            self.yaw_outspd = 1
        if self.yaw_outspd < -1:
            self.yaw_outspd = -1

        if abs(self.yaw_errP*180/math.pi) < .1:
           self.yaw_outspd = 0
        if self.yaw_outspd <= 0:
            self.left(speed=-1*self.yaw_outspd)
        if self.yaw_outspd>=0:
            self.right(speed=self.yaw_outspd)
        self.yaw_errI += self.yaw_errP*(self.t_elapsed-self.lastTime)
        time.sleep(0.01)
        self.lastTime = self.t_elapsed



