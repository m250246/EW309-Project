from MotorController import Motor
import board
import time
import usb_cdc
import math



motor = Motor(board.GP8, board.GP11, board.GP10, board.GP9, board.GP12, board.GP13, board.GP6, board.GP7)
print('\n\n\n')

Kp = .05
Ki = .01
Kd = .09
des_pos = -10 # degrees
s=1

while s:  # run indefinitely
    t_start = time.monotonic()  # clock time at start of experiment
    t_elapsed = 0.0 # variable to represent the elapsed time of the experiment
    # initial integral of p_error
    err_int = 0
    while t_elapsed < 3:
        motor.data()
        pan_rate = motor.pan_rate * (180/math.pi)
        t_elapsed = time.monotonic() - t_start # measure time since start of experiment
        p_error = des_pos - motor.panA
        err_der = 0 - pan_rate
        outspd = Kp*p_error + Ki*err_int + Kd*err_der  # PI_Lead controller
        print(motor.panA, p_error, outspd)
        if outspd > 1: # make sure motor input is between [-1,1]
            outspd = 0.9
        if outspd < -1:
            outspd = -0.9
        if outspd < 0:
            motor.left(speed=-1*outspd)
            err_int = err_int + p_error*(time.monotonic()-t_elapsed)
        if outspd>0:
            motor.right(speed=outspd)
            err_int = err_int - p_error*(time.monotonic()-t_elapsed)
        time.sleep(0.1)
    print("Finished trial") # let debugging terminal know experiment is done
    motor.stop()
    print("finished sending trial data")
    s=0




