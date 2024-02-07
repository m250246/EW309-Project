clear;
clc;
close all;
%% Data Read Log

turret_data = readtable('data.log');
turret_data = table2array(turret_data);
time = turret_data(7:180,1)-turret_data(7,1);
panA = turret_data(7:180,2);
tiltA = turret_data(7:180,3);
panRate = turret_data(7:180,5);
tiltRate = turret_data(7:180,4);



%% Plot
figure(1)
subplot(211)
plot(time, panA)
title("pan angle")

subplot(212)
plot(time, panRate)
title("pan rate")

figure(2)
subplot(211)
plot(time, tiltA)
title("tilt angle")

subplot(212)
plot(time, tiltRate)
title("tilt rate")


%%
figure(3)
h=animatedline;
axis([0 250 0 360])
xlabel('pan angle')
ylabel('tilt angle')
title('aiming direction')
for n=1:length(time)
    addpoints(h,panA(n),tiltA(n));
    drawnow;
    pause(.1);
end