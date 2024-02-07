clear;
clc;
close all;

pico = serialport('COM24',9600);
msg='Hello';
pico.writeline(msg);
fprintf("Waiting for PICO \n")
data = pico.readline();
fprintf(data)
