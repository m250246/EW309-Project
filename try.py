import serial 
import time 
pico = serial.Serial(port='COM24', baudrate=115200, timeout=1) 
pico.reset_input_buffer()
pico.reset_output_buffer()
while True:
        while pico.in_waiting>0:
            question = pico.readline().decode().strip()
            if question == 'q':
                  quit()
            var = input(str(question))
            if question == 'q':
                  quit()
            msg = str(var)+"\n"
            pico.write(msg.encode())