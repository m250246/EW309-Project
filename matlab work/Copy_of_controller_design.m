clear;
clc;
close all;
load TF_parameters.mat

%% Position TF
Gsys = TF_PAN_LR;
s = tf('s');
G_sys = Gsys/s;
rlocus(G_sys)
%% PIL
des_damping = cos(atan(1/10));
PO=100*exp((-des_damping*pi)/(sqrt(1-des_damping^2)));
ts=4/10;
[K,Gc0,sd,T, z, p] = PI_lead(G_sys,PO,ts);
%% PID GAINS
Kp=(K*z*(2*p-z))/p^2
Ki=K*z^2/p
Kd=(K-Kp)/p

KGc = Kp+(Ki/s)+Kd*s*(p/(s+p));

s=tf('s');
time = 0:0.1:5;
figure(4);
step(T, time)

%% PID GAINS
Kp=1.8
Ki=.01
Kd=.01

KGc = Kp+(Ki/s)+Kd*s*(p/(s+p));
CLTF = minreal(KGc*G_sys/(1+KGc*G_sys));

s=tf('s');
time = 0:0.1:5;
figure(5);
step(CLTF, time)