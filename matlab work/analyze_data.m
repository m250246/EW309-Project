clear;
clc;
close all;
%% Data Read Log
turret_data = readtable('data/continuous_down_up_pauses3.log');
%%
turret_data = table2array(turret_data);
time = turret_data(:,1)-turret_data(1,1);
panA = turret_data(:,2);
tiltA = turret_data(:,3);
rollA = turret_data(:,4);
panRate = turret_data(:,5);
tiltRate = turret_data(:,6);
rollRate = turret_data(:,7);


%% Plot left/right
% figure(1)
% subplot(211)
% plot(time, panA)
% xlabel('Time (s)')
% ylabel('Angular Position (deg)')
% title("Pan (LEFT/RIGHT)")
% subplot(212)
% plot(time, panRate)
% xlabel('Time (s)')
% ylabel('Angular Speed (rad/s)')

%ORRRRR up/down
figure(1)
subplot(211)
plot(time, tiltA)
xlabel('Time (s)')
ylabel('Angular Position (deg)')
title('Tilt (UP/DOWN)')
subplot(212)
plot(time, tiltRate)
xlabel('Time (s)')
ylabel('Angular Speed (rad/s)')



% figure(1)
% subplot(231)
% plot(time, panA)
% ylim([-180,180])
% title("pan")
% subplot(232)
% plot(time, tiltA)
% ylim([-90,90])
% title('tilt')
% subplot(233)
% plot(time, rollA)
% subplot(234)
% plot(time, panRate)
% ylim([-1,1])
% subplot(235)
% plot(time,tiltRate)
% ylim([-1,1])
% subplot(236)
% plot(time, rollRate)
% ylim([-1,1])

% %% Data Read Log
% 
% turret_data = readtable('up_down.log');
% %%
% turret_data = table2array(turret_data);
% time = turret_data(50:350,1)-turret_data(50,1);
% panA = turret_data(50:350,2);
% tiltA = turret_data(50:350,3);
% rollA = turret_data(50:350,4);
% panRate = turret_data(50:350,5);
% tiltRate = turret_data(50:350,6);
% rollRate = turret_data(50:350,7);
% 
% %% Plot
% figure(2)
% subplot(221)
% plot(time, panA)
% title("pan")
% subplot(222)
% plot(time, tiltA)
% title('tilt')
% subplot(223)
% plot(time, panRate)
% subplot(224)
% plot(time, tiltRate)


%%
% figure(3)
% h=animatedline;
% axis([150 200 -50 50])
% axis([0 60 340 360])
% xlabel('pan angle')
% ylabel('tilt angle')
% title('aiming direction')
% for n=1:length(time)
%     addpoints(h,panA(n),tiltA(n));
%     drawnow;
%     pause(.01);
% end