from MotorController import Motor
import board
import time
import usb_cdc
import math



motor = Motor(board.GP8, board.GP11, board.GP10, board.GP9, board.GP12, board.GP13, board.GP6, board.GP7, board.GP15, board.GP14)
print('\n\n\n')

Kp = 1.5
Ki = 0.8
Kd = 0.1
des_pos = 0*(math.pi/180) # degrees

dz_up=0.1
dz_down = 0.3

t_start = time.monotonic()  # clock time at start of experiment
t_elapsed = 0.0 # variable to represent the elapsed time of the experiment
t_prev = 0
# initial integral of errP
errI = 0
while t_elapsed < 3:
    motor.data()
    tiltA = motor.tiltA*(math.pi/180) # degrees to radians
    t_elapsed = time.monotonic() - t_start # measure time since start of experiment
    errP = des_pos - tiltA
    errD = 0 - motor.tilt_rate
    outspd = Kp*errP + Ki*errI + Kd*errD  # PI_Lead controller

    if outspd > 0:
        outspd += dz_up
    if outspd < 0:
        outspd -= dz_down

    if outspd > 1: # make sure motor input is between [-1,1]
        outspd = 1
    if outspd < -1:
        outspd = -1

    print(motor.tiltA, errP*(180/math.pi), outspd)

    if outspd < 0:
        motor.down(speed=-1*outspd)
    if outspd>0:
        motor.up(speed=outspd)
    errI += errP*(t_elapsed-t_prev)

    time.sleep(0.1)
    t_prev = t_elapsed

print("Finished trial") # let debugging terminal know experiment is done
motor.stop()
print("finished sending trial data")




