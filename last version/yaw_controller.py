from MotorController import Motor
import board
import time
import usb_cdc
import math



motor = Motor(board.GP8, board.GP11, board.GP10, board.GP9, board.GP12, board.GP13, board.GP6, board.GP7, board.GP15, board.GP14)
print('\n\n\n')

#Kp = 1.8
#Ki = .01
#Kd = .01
Kp = 1.8
Ki = .01
Kd = .01
des_pos = 25*(math.pi/180) # degrees
s=1
dz=0.17

t_start = time.monotonic()  # clock time at start of experiment
t_elapsed = 0.0 # variable to represent the elapsed time of the experiment
t_prev = 0
# initial integral of errP
errI = 0
while t_elapsed < 3:
    motor.data()
    panA = motor.panA*(math.pi/180)
    t_elapsed = time.monotonic() - t_start # measure time since start of experiment
    errP = des_pos - panA
    errD = 0 - motor.pan_rate
    outspd = Kp*errP + Ki*errI + Kd*errD  # PI_Lead controller
    if outspd > 0:
        outspd += dz
    if outspd < 0:
        outspd -= dz

    if outspd > 1: # make sure motor input is between [-1,1]
        outspd = 1
    if outspd < -1:
        outspd = -1

    print(motor.panA, errP*(180/math.pi), outspd)
    if outspd < 0:
        motor.left(speed=-1*outspd)
    if outspd>0:
        motor.right(speed=outspd)
    errI += errP*(t_elapsed-t_prev)
    time.sleep(0.1)
    t_prev = t_elapsed

print("Finished trial") # let debugging terminal know experiment is done
motor.stop()
print("finished sending trial data")




