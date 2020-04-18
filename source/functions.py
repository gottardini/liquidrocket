import numpy as np
from scipy.optimize import fsolve

def calcGasConstant(Ru,MM):
    return Ru*1e3/MM;

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

def calcAdaptedSpecificImpulse(u_e,g_0):
    return u_e/g_0

def calcAdaptedThrustCoefficient(eta_2D,I_s_e,g_0,c_star):
    return eta_2D*I_s_e*g_0/c_star

def calcThrustCoefficientWhat(p_a,y,eps,p_e,p_c):
    return np.sqrt((2*(y**2)/(y-1))*((2/(y+1))**((y+1)/(y-1))))+eps*((p_e-p_a)/p_c);

def calcThrustCoefficient(p_a,y,eps,p_e,p_c):
    return y*np.sqrt(2/(y-1)*((2/(y+1))**((y+1)/(y-1)))*(1-(p_e/p_c)**((y-1)/y)))+eps*(p_e-p_a)/p_c;

def calcPropFlowRate(T_z, u_e, eps, p_c, ct, p_e, p_z):
    return T_z/(u_e+((eps*u_e)/(p_c*ct))*(p_e-p_z));

def calcThroatArea(m_p, u_e, p_c, ct):
    return (m_p*u_e)/(p_c*ct)

def calcThroatDiameter(A_t):
    return np.sqrt(4*A_t/np.pi)

def calcExitArea(A_t,eps):
    return A_t*eps

def calcExitDiameter(A_e):
    return np.sqrt(4*A_e/np.pi)

def calcThrust(m_p, u_e, A_e, p_e, p_a):
    return m_p*u_e + (p_e-p_a)*A_e

def calcTropoPressure(z,p_0,T_0,a,g_0, R_air):
    return p_0*(1+a*z/T_0)**(-g_0/(a*R_air))

def calcPressureFromAltitude(z,p_0,T_0,a,g_0, R_air):
    return np.where(z<=11e3,calcTropoPressure(z,p_0,T_0,a,g_0, R_air),calcTropoPressure(11e3,p_0,T_0,a,g_0, R_air)*np.exp(-g_0*(z-11e3)/(R_air*(T_0-a*11e3))))

def calcAltitudeFromPressure(p,p_0,T_0,a,g_0, R_air):
    return np.where(p<=calcTropoPressure(11e3,p_0,T_0,a,g_0, R_air),11e3-R_air*(T_0-a*11e3)*np.log(p/calcTropoPressure(11e3,p_0,T_0,a,g_0, R_air))/g_0,calcTropoAltitude(p,p_0,T_0,a,g_0, R_air))

def calcTropoAltitude(p,p_0,T_0,a,g_0, R_air):
    return T_0/a*((p/p_0)**(-a*R_air/g_0)-1)

def kiloNewtonToNewton(f):
    return 1e3*f
