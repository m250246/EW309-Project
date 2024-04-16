clear;
clc;
close all;
%% Data Read Log
% all data at speed 1
%% LEFT DATA
turret_data = readtable('data/left.log');
turret_data = table2array(turret_data);
time = turret_data(10:30,1)-turret_data(10,1);
panRate = turret_data(10:30,5);

%% Calculate SSV and TConst @63%
% figure(1);
% plot(time, panRate);
% xlabel('Time');
% ylabel('Angular Speed (rad/s)')
% title('Pan Rate')
ssH = mean(panRate(10:end));
[val,idx]=min(abs(panRate-(.63*ssH)));
tconst = time(idx)/2; % NOTE: tconst moved back
%% First Order Transfer Function
v=1;
s = tf('s');
A_dc = ssH/v;
apan = 1/tconst;
bpan = apan*A_dc;
Gtf = bpan/(s+apan);
simTime = 0:.1:2;
%% COMPARE
[simLeft, t]=step(v*Gtf, simTime);
figure(1);
plot(time, panRate);
hold on;
plot(t,simLeft);
legend('Experimental','Simulated')
xlabel('Time');
ylabel('Angular Speed (rad/s)')
title('Transfer Function: LEFT')

%% RIGHT DATA
turret_data = readtable('data/right.log');
turret_data = table2array(turret_data);
time = turret_data(10:30,1)-turret_data(10,1);
panRate = abs(turret_data(10:30,5));
%% COMPARE LEFT/RIGHT
[simRight, t]=step(v*Gtf, simTime);
figure(2);
plot(time, panRate);
hold on;
plot(t,simRight);
legend('Experimental','Simulated')
xlabel('Time');
ylabel('Angular Speed (rad/s)')
title('Transfer Function: RIGHT')
TF_PAN_LR = Gtf

%% UP DATA
turret_data = readtable('data/up.log');
turret_data = table2array(turret_data);
time = turret_data(88:210,1)-turret_data(88,1);
tiltRate = abs(turret_data(88:210,6));

%% Calculate SSV and TConst @63%
% figure(1);
% plot(time, panRate);
% xlabel('Time');
% ylabel('Angular Speed (rad/s)')
% title('Pan Rate')
ssH = mean(tiltRate(10:end));
[val,idx]=min(abs(tiltRate-(.63*ssH)));
tconst = time(idx); % NOTE: tconst moved back
%% First Order Transfer Function
v=1;
s = tf('s');
A_dc = ssH/v;
atilt = 1/tconst;
btilt = atilt*A_dc;
Gtf = btilt/(s+atilt);
simTime = 0:.01:1.4;
%% COMPARE SIM/EXP
[simUP, t]=step(v*Gtf, simTime);
figure(3);
plot(time, tiltRate);
hold on;
plot(t,simUP);
legend('Experimental','Simulated')
xlabel('Time');
ylabel('Angular Speed (rad/s)')
title('Transfer Function: UP')
TF_TILT_UP = Gtf

%% DOWN DATA
turret_data = readtable('data/down.log');
turret_data = table2array(turret_data);
time = turret_data(88:210,1)-turret_data(88,1);
tiltRate = abs(turret_data(88:210,6));
%% Calculate SSV and TConst @63%
% figure(1);
% plot(time, panRate);
% xlabel('Time');
% ylabel('Angular Speed (rad/s)')
% title('Pan Rate')
ssH = mean(tiltRate(10:end));
[val,idx]=min(abs(tiltRate-(.63*ssH)));
tconst = time(idx)/1.5; % NOTE: 
%% First Order Transfer Function
v=1;
s = tf('s');
A_dc = ssH/v;
atilt = 1/tconst;
btilt = atilt*A_dc;
Gtf = btilt/(s+atilt);
simTime = 0:.01:1.4;
%% COMPARE SIM/EXP
[simDown, t]=step(v*Gtf, simTime);
figure(4);
plot(time, tiltRate);
hold on;
plot(t,simDown);
legend('Experimental','Simulated')
xlabel('Time');
ylabel('Angular Speed (rad/s)')
title('Transfer Function: DOWN')
TF_TILT_DOWN = Gtf

save('TF_parameters.mat', 'TF_PAN_LR', 'TF_TILT_DOWN', 'TF_TILT_UP')

