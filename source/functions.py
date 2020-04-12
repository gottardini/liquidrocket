import numpy as np
from scipy.optimize import fsolve

def calcGasConstant(Ru,MM):
    return Ru/MM;

def vanker(y):
    return np.sqrt(y*(2/(y+1))**((y+1)/(y-1)));

def calcExitPressure(gasGamma,chamberPressure,nozzleEpsilon,pressureGuess):
    f = lambda x: 1/nozzleEpsilon - (((gasGamma+1)/2)**(1/(gasGamma-1)))* \
    np.sqrt((gasGamma+1)/(gasGamma-1))*((x/chamberPressure)**(1/gasGamma))* \
    np.sqrt(1-(x/chamberPressure)**((gasGamma-1)/gasGamma));
    return fsolve(f,pressureGuess)

def calcCharacteristicVelocity(R_cp,T_c,GAMMA):
    return np.sqrt(R_cp*T_c)/GAMMA

def calcExitVelocity(eta_2D,y,R_cp,T_c,p_e,p_c):
    return eta_2D*np.sqrt(2*(y/(y-1))*R_cp*T_c*(1-(p_e/p_c)**((y-1)/y)));

def calcSpecificImpulse(u_e,g_0):
    return u_e/g_0

def calcThrustCoefficient(eta_2D,I_s_e,g_0,c_star):
    return eta_2D*I_s_e*g_0/c_star

def calcPropFlowRate(T_z, u_e, eps, p_c, c_t_e, p_e, p_z):
    return T_z/(u_e+((eps*u_e)/(p_c*c_t_e))*(p_e-p_z));

def calcThroatArea(m_p, u_e, p_c, c_t_e):
    return (m_p*u_e)/(p_c*c_t_e)

def calcThroatDiameter(A_t):
    return np.sqrt(4*A_t/np.pi)

def calcExitArea(A_t,eps):
    return A_t*eps

def calcExitDiameter(A_e):
    return np.sqrt(4*A_e/np.pi)
