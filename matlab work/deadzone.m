close all;
clear;
clc;

%% Load Data
turret_data = readtable('dead zone\up_dead.log');
turret_data = table2array(turret_data);
time = turret_data(:,1);
panRate = turret_data(:,2);
tiltRate = turret_data(:,3);
speedIN = turret_data(:,4);

plot(speedIN, tiltRate, 'o')

%% LEFT = 0.19
%% RIGHT = 0.2
%% UP = 0.15
%% DOWN = 0.35