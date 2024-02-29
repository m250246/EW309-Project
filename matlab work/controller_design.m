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
PO = 0.1; % percent
ts = 4/10; %[sec] BASED ON BREAK AWAY PT
[K,Gc0,sd,T, z, p] = PI_lead(G_sys,PO,ts);
%% PID GAINS
Kp(1)=(K*z*(2*p-z))/p^2
Ki(1)=K*z^2/p
Kd(1)=(K-Kp)/p
% 
% Ki(1)=K*(z1*z2)/p
% Kp(1)=((K*(z1+z2))-Ki)/p
% Kd(1)=(K-Kp)/p

KGc = Kp+(Ki/s)+Kd*s*(p/(s+p));
s=tf('s');
Gc = tf(KGc/K);
Gc=tf(Gc);
%% sim
V_0 = 0.2;
des_pos = deg2rad(45);
G_new = G_sys;
out = sim("PIL.slx");
simT=out.pos.Time;
simP = out.pos.Data;
simV = out.volt.Data;
%% charac
ry = stepinfo(simP, simT, des_pos);
ru = stepinfo(simV, simT);
SettlingTime(1) = ry.SettlingTime;
Overshoot(1) = ry.Overshoot;
MaxIn(1) = ru.Peak;
%% Simulated and Iterate 

figure(4);
xlabel('Time')
subplot(2,1,1)
plot(simT, simP)
ylabel("Position")
xlabel("Time")
hold on;
subplot(2,1,2)
plot(simT, simV)
ylabel("Volts")
xlabel("Time")
% hold on;
% i=2;
% cont = 1;
% %% iterate
% while cont == 1
%     Kp(i)=input("Kp: ");
%     Ki(i)=input("Ki: ");
