from models import *
from source.functions import *
import numpy as np

flight={
    'z':InputVariable("Quota [m]",np.linspace(0,1e5,50)),
}

atmoshpere={
    'p':UnknownVariable("Pressione atmosferica",CalcFunction(calcPressureFromAltitude,'z','p_0','T_0','a','g_0','R_air')),
    #"p_tropo':UnknownVariable("Pressione troposferica",CalcFunction(calcTropoPressure,'z','p_0','T_0','a','g_0','R_air')),
}

global_constants={
    'R_u':InputVariable("Costante dei gas ideali", 8.31446261815324), # [J/(mol*K)]
    'g_0':InputVariable("Accelerazione gravitzionale a quota zero", 9.807), # [m/s^2]
    'a':InputVariable("Gradiente di temperatura verticale",0.0065), # [K/m]
    'p_0':InputVariable("Pressione a quota zero", 101325), # [Pa]
    'T_0':InputVariable("Temperatura a quota zero", 288.16), # [K]
    'GUESS':InputVariable("Stima pressione all'efflusso",20000),
    'R_air':InputVariable("Costante specifica dell'aria",287.058),
}

variables_cea={
    'cc_cea':UnknownVariable("Oggetto CEA per la camera di combustione",CalcFunction(getCeaObj,'fuelName','oxName')),
    'pb_cea':UnknownVariable("Oggetto CEA per il preburner",CalcFunction(getCeaObj,'fuelName','oxName')),
}

outflow_gases={
    #CEA DATA
    'Mm_cc_e':UnknownVariable("Massa molare dei gas combusti",CalcFunction(getCeaThroatMM,'cc_cea','p_cc','r_cc','eps')),
    'y_cc_e':UnknownVariable("Rapporto calori specifici dei gas combusti",CalcFunction(getCeaThroatGam,'cc_cea','p_cc','r_cc','eps')),
    'T_cc':UnknownVariable("Temperatura alla fine della camera di combustione",CalcFunction(getCeaThroatTemperature,'cc_cea','p_cc','r_cc','eps')),

    #OTHER DATA
    'R_cc_e':UnknownVariable("Costante dei gas di scarico",CalcFunction(calcGasConstant,'R_u','Mm_cc_e')),
    'GAMMA':UnknownVariable("Funzione di Van Kerckhove",CalcFunction(vanker,'y_cc_e')),
    'p_e':UnknownVariable("Pressione all'efflusso",CalcFunction(calcExitPressure,'y_cc_e','p_cc','eps','GUESS')),
    'u_e':UnknownVariable("Velocità all'efflusso",CalcFunction(calcExitVelocity,'eta_2D','y_cc_e','R_cc_e','T_cc','p_e','p_cc')),
    'c_star':UnknownVariable("Velocità caratteristica",CalcFunction(calcCharacteristicVelocity,'R_cc_e','T_cc','GAMMA')),

    'm_p':UnknownVariable("Portata massica di propellente",CalcFunction(calcPropFlowRate,'thr_n','u_e','eps','p_cc','ct_n','p_e','p_n')),
}

combustion_chamber={
    #CEA DATA
    'Mm_cc_c':UnknownVariable("Massa molare dei gas in camera di combustione",CalcFunction(getCeaChamberMM,'cc_cea','p_cc','r_cc','eps')),
    'y_cc_c':UnknownVariable("Rapporto calori specifici dei gas combusti",CalcFunction(getCeaThroatGam,'cc_cea','p_cc','r_cc','eps')),

    #OTHER
    'R_cc_c':UnknownVariable("Costante specifica dei gas in camera di combustione",CalcFunction(calcGasConstant,'R_u','Mm_cc_c')),
    'Ma_c':InputVariable("Numero di Mach in camera di combustione", 0.2),
    'C_d':InputVariable("Coefficiente di efflusso piastra di iniezione", 0.88),
    'alpha_ox':InputVariable("Inclinazione linea iniezione ossidante[rad]", 0.5236),
    'u_c':UnknownVariable("Velocità in camera di combustione", CalcFunction(calcChamberVelocity, 'Ma_c', 'y_cc_c', 'R_cc_c', 'T_cc')),
    'rho_c':UnknownVariable("Densità dei gas in camera di combustione", CalcFunction(calcDensity, 'p_cc', 'R_cc_c', 'T_cc')),
    'A_c':UnknownVariable("Area camera di combustione", CalcFunction(calcChamberArea, 'm_p', 'rho_c', 'u_c')),
    'D_c':UnknownVariable("Diametro camera di combustione", CalcFunction(calcDiameter, 'A_c')),
    'V_c':UnknownVariable("Volume camera di combustione", CalcFunction(calcChamberVolume, 'L_star', 'A_c')),
    'L_c':UnknownVariable("Lunghezza camera di combustione", CalcFunction(calcChamberLength, 'V_c', 'A_c')),
    'A_th_f':UnknownVariable("Area di tutti i fori piastra combustibile", CalcFunction(calcTotalHolesArea, 'm_f', 'C_d', 'rho_f', 'p_loss_inj', 'p_cc')),
    'A_th_ox':UnknownVariable("Area di tutti i fori piastra ossidante", CalcFunction(calcTotalHolesArea, 'm_ox', 'C_d', 'rho_ox', 'p_loss_inj', 'p_cc')),
    'n_h_f':UnknownVariable("Numero di fori piastra combustibile di diametro 1mm", CalcFunction(calcNumber1Holes, 'A_th_f')),
    'n_h_ox':UnknownVariable("Numero di fori piastra ossidante di diametro 1mm", CalcFunction(calcNumber1Holes, 'A_th_ox')),
    'n_h':UnknownVariable("Numero di fori di ciascunna linea", CalcFunction(calcNumberHoles, 'n_h_f', 'n_h_ox')),
    'A_1h_f':UnknownVariable("Area di un foro-combustibile", CalcFunction(calcHoleArea, 'A_th_f', 'n_h')),
    'A_1h_ox':UnknownVariable("Area di un foro-ossidante", CalcFunction(calcHoleArea, 'A_th_ox', 'n_h')),
    'D_1h_f':UnknownVariable("Diametro di un foro-combustibile", CalcFunction(calcDiameter, 'A_1h_f')),
    'D_1h_ox':UnknownVariable("Diametro di un foro-ossidante", CalcFunction(calcDiameter, 'A_1h_ox')),
    'u_f':UnknownVariable("Velocità iniezione combustibile", CalcFunction(calcInjectionVelocity, 'C_d', 'p_loss_inj', 'p_cc', 'rho_f')),
    'u_ox':UnknownVariable("Velocità iniezione ossidante", CalcFunction(calcInjectionVelocity, 'C_d', 'p_loss_inj', 'p_cc', 'rho_ox')),
    'alpha_f':UnknownVariable("Inclinazione linea iniezione combustibile", CalcFunction(calcFuelInjectionAngle, 'm_ox', 'm_f', 'u_ox', 'u_f', 'alpha_ox')),
}

feed_system_constants={
    'p_loss_inj':InputVariable("Frazione perdite di carico piastra di iniezione",0.2),
    'p_loss_exc':InputVariable("Frazione perdite di carico scambiatore di calore",0.15),
    'p_loss_feed':InputVariable("Frazione perdite di carico linee di alimentazione",0.1),
    'p_loss_valves':InputVariable("Frazione perdite di carico valvole",0.15),
    'r_pb':InputVariable("Rapporto massico di miscela preburner",0.9),
    'eta_pump_f':InputVariable("Rendimento della pompa di combustibile",1),
    'eta_pump_ox':InputVariable("Rendimento della pompa di ossidante",1),
    'eta_mt':InputVariable("Rendimento meccanico della turbina",1),
    'eta_ad':InputVariable("Rendimento adiabatico della turbina",1),
    'p_out_pb':InputVariable("Pressione di uscita turbina",300000), #non lo so, a caso
    'p_cpb':InputVariable("Pressione di combustione preburner",1e7) #non lo so, a caso
}

preburner={
    'cp_pb':UnknownVariable("C_p preburner",CalcFunction(getCeaChamberCp,'pb_cea','p_pb','r_pb')),
    'T_pb':UnknownVariable("Temperatura preburner",CalcFunction(getCeaChamberTemperature,'pb_cea','p_pb','r_pb')),
    'y_pb':UnknownVariable("Rapporto calori specifici preburner",CalcFunction(getCeaThroatGam,'pb_cea','p_pb','r_pb','eps')),
}

feed_system_variables={
    'm_f':UnknownVariable("Portata massica di combustibile",CalcFunction(calcFuelRate,'m_p','r_cc')),
    'm_ox':UnknownVariable("Portata massica di ossidante", CalcFunction(calcOxidizerRate, 'm_f', 'r_cc')),
    'pstar_f':UnknownVariable("Pressione combustibile a valle della pompa",CalcFunction(calcPStarF,'p_cc','p_loss_inj','p_loss_exc','p_loss_feed','p_loss_valves')),
    'pstar_ox':UnknownVariable("Pressione ossidante a valle della pompa",CalcFunction(calcPStarOx,'p_cc','p_loss_inj','p_loss_feed','p_loss_valves')),
    'deltap_pump_f':UnknownVariable("Delta P pompa combustibile",CalcFunction(lambda pstar,ptank: pstar-ptank,'pstar_f','p_tank_f')),
    'deltap_pump_ox':UnknownVariable("Delta P pompa ossidante",CalcFunction(lambda pstar,ptank: pstar-ptank,'pstar_ox','p_tank_ox')),
    'q_eng_f':UnknownVariable("Portata volumetrica di combustibile al motore",CalcFunction(lambda m,rho: m/rho,'m_f','rho_f')),
    'q_eng_ox':UnknownVariable("Portata volumetrica di ossidante al motore",CalcFunction(lambda m,rho: m/rho,'m_ox','rho_ox')),
    'q_spil_f':UnknownVariable("Portata volumetrica di combustibile spillato",CalcFunction(calcSpilF,'q_eng_f','deltap_pump_f','deltap_pump_ox','eta_pump_f','eta_pump_ox','rho_f','rho_ox','r_cc','r_pb','eta_mt','eta_ad','cp_pb','T_pb','p_out_pb','p_pb','y_pb')),
    'q_tot_f':UnknownVariable("Portata volumetrica totale di combustibile",CalcFunction(lambda qsp,qeng: qsp+qeng,'q_spil_f','q_eng_f')),
    'q_spil_ox':UnknownVariable("Portata volumetrica di ossidante spillato",CalcFunction(lambda qspf,tau,rhof,rhoox: qspf*tau*rhof/rhoox,'q_spil_f','r_pb','rho_f','rho_ox')),
    'q_tot_ox':UnknownVariable("Portata volumetrica totale di ossidante",CalcFunction(lambda qsp,qeng: qsp+qeng,'q_spil_ox','q_eng_ox')),
    'm_tot_f':UnknownVariable("Portata massica di combustibile totale",CalcFunction(lambda q,rho: q*rho,'q_tot_f','rho_f')),
    'm_tot_ox':UnknownVariable("Portata massica di ossidante totale",CalcFunction(lambda q,rho: q*rho,'q_tot_ox','rho_ox')),
}

static_propulsive_parameters={
    'thr_ad':UnknownVariable("Spinta a quota di adattamento",CalcFunction(calcThrust,'m_p','u_e','A_e','p_e', 'p_e')),
    'z_ad':UnknownVariable("Quota di adattamento",CalcFunction(calcAltitudeFromPressure,'p_e','p_0','T_0','a','g_0','R_air')),
    'thr_n':UnknownVariable("Spinta nominale",CalcFunction(kiloNewtonToNewton,'T_n')),
    'Is_ad':UnknownVariable("Impulso specifico a quota di adattamento",CalcFunction(calcAdaptedSpecificImpulse,'u_e','g_0')),
    'ct_ad':UnknownVariable("Coefficiente di spinta a quota di adattamento",CalcFunction(calcAdaptedThrustCoefficient,'eta_2D','Is_ad','g_0','c_star')),
    'ct_n':UnknownVariable("Coefficiente di spinta nominale",CalcFunction(calcThrustCoefficient,'p_n', 'y_cc_e', 'eps', 'p_e', 'p_cc')),
}

nonstatic_propulsive_parameters={
    'ct_var':UnknownVariable("Coefficiente di spinta",CalcFunction(calcThrustCoefficient,'p','y_cc_e','eps','p_e','p_cc')),
    'thr_var':UnknownVariable("Spinta",CalcFunction(calcThrust,'m_p','u_e','A_e','p_e', 'p')),
    'I_s':UnknownVariable("Impulso specifico", CalcFunction(calcSpecificImpulse, 'thr_var', 'm_p', 'g_0')),
    'I_v':UnknownVariable("Impulso specifico volumetrico", CalcFunction(calcVolumetricSpecificImpulse, 'I_s', 'rho_avg')),
    'I_tot':UnknownVariable("Impulso specifico totale", CalcFunction(calcTotalVolumetricImpulse, 'I_s', 'M_ox', 'M_f', 'g_0'))
}

nozzle={
    'theta':UnknownVariable("Half expansion angle", np.pi/12),#CAPIRE SE È DATO GLOBALE O RELATIVO AL SINGOLO STADIO. SE RELATIVO, ALLORA AGGIUNGI SU GOOGLE SPREADSHEET
    'A_t':UnknownVariable("Sezione di gola",CalcFunction(calcThroatArea,'m_p','u_e','p_cc','ct_n')),
    'D_t':UnknownVariable("Diametro di gola",CalcFunction(calcDiameter,'A_t')),
    'A_e':UnknownVariable("Area di efflusso",CalcFunction(calcExitArea,'eps','A_t')),
    'D_e':UnknownVariable("Diametro di efflusso",CalcFunction(calcDiameter,'A_e')),
    'L_cone':UnknownVariable("Lunghezza cono", CalcFunction(calcConeLength, 'eps', 'D_t', 'theta')),
    'L_bell':UnknownVariable("Lunghezza campana", CalcFunction(calcBellLength, 'L_cone')),#CALCOLATA ALL'80% DI L_cone
    'theta_i':UnknownVariable("Angolo iniziale tratto convergente", CalcFunction(calcThetai, 'D_c', 'D_t')),
    'x_conv':UnknownVariable("Array contenente coordinate x dei punti della funzione, il cui grafico "
                             "disegna il tratto convergente dell'ugello", CalcFunction(calcXConv, 'theta_i', 'D_t')),
    'y_conv':UnknownVariable("Array contenente coordinate y dei punti della funzione, il cui grafico "
                             "disegna il tratto convergente dell'ugello", CalcFunction(calcYConv, 'theta_i', 'D_t')),
    'x_div_plus':UnknownVariable("Array contenente coordinate x dei punti della funzione, il cui grafico disegna il "
                                 "tratto divergente a concavità verso l'alto dell'ugello", CalcFunction(calcXDivPlus, 'theta_n', 'D_t')),
    'y_div_plus':UnknownVariable("Array contenente coordinate y dei punti della funzione, il cui grafico disegna il "
                                 "tratto divergente a concavità verso l'alto dell'ugello", CalcFunction(calcYDivPlus,'theta_n', 'D_t')),
    'x_div_minus':UnknownVariable("Array contenente coordinate x dei punti della funzione, il cui grafico disegna il "
                                 "tratto divergente a concavità verso il basso dell'ugello", CalcFunction(calcXDivMinus, 'theta_n', 'theta_e', 'D_t', 'L_bell', 'D_e')),
    'y_div_minus':UnknownVariable("Array contenente coordinate y dei punti della funzione, il cui grafico disegna il "
                                 "tratto divergente a concavità verso il basso dell'ugello", CalcFunction(calcYDivMinus, 'theta_n', 'theta_e', 'D_t', 'L_bell', 'D_e')),
#DISEGNAMO METÀ UGELLO, SOLO LA PARTE SOPRA. TROVARE MODO PER FARE MIRROR
}

tanks={
    'M_f':UnknownVariable("Massa di combustibile", CalcFunction(calcMass, 'm_f', 't_b', 'k_s')),
    'M_ox':UnknownVariable("Massa di ossidante", CalcFunction(calcMass, 'm_ox', 't_b', 'k_s')),
    'V_f':UnknownVariable("Volume di combustibile", CalcFunction(calcVolume, 'M_f', 'rho_f')),
    'V_ox':UnknownVariable("Volume di ossidante", CalcFunction(calcVolume, 'M_ox', 'rho_ox')),
    'rho_avg':UnknownVariable("Densità media propellente", CalcFunction(calcRhoAvg, 'M_f', 'M_ox', 'V_f', 'V_ox')),
    'k_s':InputVariable("Coefficiente di sicurezza massa", 1.05),
}
