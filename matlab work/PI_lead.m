function [K,Gc,sd,T, z_PIL, p_lead] = PI_lead(G,PO,ts)
    z = abs(log(PO/100)/pi)/sqrt(1+(log(PO/100)/pi)^2);
    wn = 4/(z*ts);
    wd = wn*sqrt(1-z^2);
    
    sd = -z*wn+1i*wd;
    
    theta_sys = angle(evalfr(G,sd));
    theta_c = 180-rad2deg(theta_sys);
    
    z_PID = z*wn+imag(sd)/tan(0.5*((deg2rad(theta_c)+angle(sd))));
    z_PIL = z_PID/2;
    
    %z1=-1*real(sd);
    %theta_z1 = rad2deg(angle(sd+z1));

    theta_z = rad2deg(angle(sd+z_PIL));
    
    %theta_p = theta_z1+theta_z-theta_c-rad2deg(angle(sd)); %change
    theta_p = 2*theta_z-theta_c-rad2deg(angle(sd)); %change
    
    p_lead = -real(sd)+wd/tan(deg2rad(theta_p));
    
    s=zpk('s');
    Gc = minreal((s+z_PIL)^2/(s*(s+p_lead)));
    %Gc=((s+z_PIL)*(s+z1))/(s*(s+p_lead));
    K=1/(abs(evalfr(Gc,sd))*abs(evalfr(G,sd)));
    T = minreal(K*Gc*G/(1+K*Gc*G));
end