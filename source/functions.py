import numpy as np
from scipy.optimize import fsolve
from rocketcea.cea_obj import CEA_Obj

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

def calcFuelRate(m_p,r):
    return m_p/(r+1)

def calcOxidizerRate(m_f, r):
    return r*m_f

def calcMass(m, t_b, k_s):
    return m*t_b*k_s

def calcVolume(M, rho):
    return M/rho

def calcRhoAvg(M_f, M_ox, V_f, V_ox):
    return (M_f+M_ox)/(V_f+V_ox)

def calcSpecificImpulse(thr, m_p, g_0):
    return np.divide(thr, m_p*g_0)

def calcVolumetricSpecificImpulse(I_s, rho_avg):
    return I_s*rho_avg

def calcTotalVolumetricImpulse(I_s, M_ox, M_f, g_0):
    return I_s*(M_ox+M_f)*g_0

def calcPStarF(p_c,P_loss_inj,P_loss_exc,P_loss_feed,P_loss_valves):
    return p_c*(1-P_loss_inj-P_loss_exc-P_loss_feed-P_loss_valves)

def calcPStarOx(p_c,P_loss_inj,P_loss_feed,P_loss_valves):
    return p_c*(1-P_loss_inj-P_loss_feed-P_loss_valves)

def getCeaOutput(fuelName, oxName,p_c, r, eps):
    ispObj = CEA_Obj( oxName=oxName, fuelName=fuelName)
    return ispObj.get_full_cea_output( Pc=p_c*1e-5, MR=r, eps=eps, short_output=1, pc_units='bar', frozenAtThroat=1)

def calcSpilF(q_eng_f,deltap_pump_f,deltap_pump_ox,eta_pump_f,eta_pump_ox,rho_f,rho_ox,tau_cc,tau_pb,eta_mt,eta_ad,cp_cpb,T_c,p_out,p_c,y_cpb):
    psi=lambda tau: tau*rho_f/rho_ox
    bl=lambda tau: deltap_pump_f/eta_pump_f + psi(tau)*deltap_pump_ox/eta_pump_ox
    denp=rho_f*(1+tau_pb)*eta_mt*eta_ad*cp_cpb*T_c*(1-(p_out/p_c)**((y_cpb-1)/y_cpb))
    return bl(tau_cc)/(denp+bl(tau_pb))*q_eng_f
