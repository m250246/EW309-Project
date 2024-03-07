import time
import usb_cdc
from MotorController import Motor
import sys

class Act():
    def __init__(self):
        self.motor = MotorController()


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

    def test_data(self, setspeed):
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
