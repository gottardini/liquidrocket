import numpy as np
from scipy.optimize import fsolve

def calcGasConstant(Ru,MM):
    return Ru/MM;

def vanker(y):
    return sqrt(y*(2/(y+1))^((y+1)/(y-1)));

def calcExitPressure(gasGamma,chamberPressure,nozzleEpsilon,pressureGuess):
    f = lambda x: 1/nozzleEpsilon - (((gasGamma+1)/2)^(1/(gasGamma-1)))* \
    sqrt((gasGamma+1)/(gasGamma-1))*((x/chamberPressure)^(1/gasGamma))* \
    sqrt(1-(x/chamberPressure)^((gasGamma-1)/gasGamma));
    return fsolve(f,pressureGuess)

def calcCharacteristicVelocity(R_cp,T_c,GAMMA):
    return sqrt(R_cp*T_c)/GAMMA

def calcExitVelocity(eta_2D,y,R_cp,T_c,p_e,p_c):
    return eta_2D*sqrt(2*(y/(y-1))*R_cp*T_c*(1-(p_e/p_c)^((y-1)/y)));

def calcSpecificImpulse(u_e,g_0):
    return u_e/g_0

def calcThrustCoefficient(eta_2D,I_s_e,g_0,c_star):
    return eta_2D*I_s_e*g_0/c_star
