clear;
clc;
close all;
load TF_parameters.mat

%% Position TF
Gsys = TF_PAN_LR;
s = tf('s');
G_sys = Gsys/s;
rlocus(Gsys)
hold on
rlocus(G_sys)
%% PIL
des_damping = cos(atan(.1/10));
PO=100*exp((-des_damping*pi)/(sqrt(1-des_damping^2)));
ts=4/10;
[K,Gc0,sd,T, z, p] = PI_lead(G_sys,PO,ts);
%% PID GAINS
Kp=(K*z*(2*p-z))/p^2
Ki=K*z^2/p
Kd=(K-Kp)/p
% 
% Ki(1)=K*(z1*z2)/p
% Kp(1)=((K*(z1+z2))-Ki)/p
% Kd(1)=(K-Kp)/p

KGc = Kp+(Ki/s)+Kd*s*(p/(s+p));
s=tf('s');
Gc = tf(KGc/K);
Gc=tf(Gc);
tf = KGc*Gsys/(1+KGc*Gsys);
time = 0:0.1:5;
figure(4);
step(tf, time)

