from models import *
from source.functions import *
import numpy as np

### DEPRECATED, NOW INJECTED FOR EACH STAGE
#flight={
#    'z':InputVariable("Quota",'m',np.linspace(0,200e3,500)),
#}

atmoshpere={
    'p':UnknownVariable("Pressione atmosferica",'Pa',CalcFunction(calcPressureFromAltitude,'z','p_0','T_0','a','g_0','R_air')),
    'p_vac':InputVariable("Pressione nel vuoto",'Pa',0),
    #"p_tropo':UnknownVariable("Pressione troposferica",CalcFunction(calcTropoPressure,'z','p_0','T_0','a','g_0','R_air')),
}

global_constants={
    'R_u':InputVariable("Costante dei gas ideali", 'J/(mol*K)',8.31446261815324),
    'g_0':InputVariable("Accelerazione gravitzionale a quota zero",'m/s^2', 9.807),
    'a':InputVariable("Gradiente di temperatura verticale",'K/m',0.0065),
    'p_0':InputVariable("Pressione a quota zero",'Pa', 101325),
    'T_0':InputVariable("Temperatura a quota zero",'K', 288.16),
    'R_air':InputVariable("Costante specifica dell'aria",'J/(kg*K)',287.058),
}

variables_cea={
    'cc_cea':UnknownVariable("Oggetto CEA per la camera di combustione",'-',CalcFunction(getCeaObj,'fuelName','oxName')),
    'cc_cea_su':UnknownVariable("Oggetto CEA per la camera di combustione con unita di misura imperiali",'-',CalcFunction(getCeaObjSU,'fuelName','oxName')),
    'pb_cea':UnknownVariable("Oggetto CEA per il preburner",'-',CalcFunction(getCeaObj,'fuelName','oxName')),
    'full_output_cea':UnknownVariable("Full Output CEA", 'No units', CalcFunction(getCeaFullOutput, 'cc_cea_su', 'p_cc', 'r_cc', 'eps'))
}

outflow_gases={
    #CEA DATA
    'Mm_cc_e':UnknownVariable("Massa molare dei gas combusti",'kg/kmol',CalcFunction(getCeaThroatMM,'cc_cea','p_cc','r_cc','eps')),
    'y_cc_e':UnknownVariable("Rapporto calori specifici dei gas combusti",'-',CalcFunction(getCeaThroatGam,'cc_cea','p_cc','r_cc','eps')),
    'T_cc':UnknownVariable("Temperatura alla fine della camera di combustione",'K',CalcFunction(getCeaThroatTemperature,'cc_cea','p_cc','r_cc','eps')),

    #OTHER DATA
    'R_cc_e':UnknownVariable("Costante dei gas di scarico",'J/(kg*K)',CalcFunction(calcGasConstant,'R_u','Mm_cc_e')),
    'GAMMA':UnknownVariable("Funzione di Van Kerckhove",'-',CalcFunction(vanker,'y_cc_e')),
    'p_e':UnknownVariable("Pressione all'efflusso",'Pa',CalcFunction(calcExitPressure,'y_cc_e','p_cc','eps','GUESS')),
    'm_p':UnknownVariable("Portata massica di propellente",'kg/s',CalcFunction(calcPropFlowRate,'thr_n','u_e','eps','p_cc','ct_n','p_e','p_n')),

    #ANALYTICAL VALUES
    'u_e':UnknownVariable("Velocità all'efflusso",'m/s',CalcFunction(calcExitVelocity,'eta_2D','y_cc_e','R_cc_e','T_cc','p_e','p_cc')),
    'c_star':UnknownVariable("Velocità caratteristica",'m/s',CalcFunction(calcCharacteristicVelocity,'R_cc_e','T_cc','GAMMA')),

    #CEA VALUES
    #'c_star':UnknownVariable("Velocità caratteristica",'m/s',CalcFunction(getCeaCharacteristicVelocity, 'cc_cea', 'p_cc', 'r_cc',iter=True)),
    #'u_e':UnknownVariable("Velocità all'efflusso",'m/s',CalcFunction(getCeaExitVelocity, 'cc_cea', 'p_cc', 'r_cc', 'eps')),
}

combustion_chamber={
    #CEA DATA
    'Mm_cc_c':UnknownVariable("Massa molare dei gas in camera di combustione",'kg/kmol',CalcFunction(getCeaChamberMM,'cc_cea','p_cc','r_cc','eps')),
    'y_cc_c':UnknownVariable("Rapporto calori specifici dei gas combusti",'-',CalcFunction(getCeaThroatGam,'cc_cea','p_cc','r_cc','eps')),

    #OTHER
    'R_cc_c':UnknownVariable("Costante specifica dei gas in camera di combustione",'J/(kg*K)',CalcFunction(calcGasConstant,'R_u','Mm_cc_c')),
    'Ma_c':InputVariable("Numero di Mach in camera di combustione",'-', 0.2),
    'C_d':InputVariable("Coefficiente di efflusso piastra di iniezione",'-', 0.88),
    'alpha_ox':InputVariable("Inclinazione linea iniezione ossidante",'rad', 0.5236),
    'u_c':UnknownVariable("Velocità in camera di combustione",'m/s', CalcFunction(calcChamberVelocity, 'Ma_c', 'y_cc_c', 'R_cc_c', 'T_cc')),
    'rho_c':UnknownVariable("Densità dei gas in camera di combustione",'kg/m^3', CalcFunction(calcDensity, 'p_cc', 'R_cc_c', 'T_cc')),
    'A_c':UnknownVariable("Area camera di combustione",'m^2', CalcFunction(calcChamberArea, 'm_p', 'rho_c', 'u_c')),
    'D_c':UnknownVariable("Diametro camera di combustione",'m', CalcFunction(calcDiameter, 'A_c')),
    'V_c':UnknownVariable("Volume camera di combustione",'m^3', CalcFunction(calcChamberVolume, 'L_star', 'A_t')),
    'L_c':UnknownVariable("Lunghezza camera di combustione",'m', CalcFunction(calcChamberLength, 'V_c', 'A_c')),
    'A_th_f':UnknownVariable("Area di tutti i fori piastra combustibile",'m^2', CalcFunction(calcTotalHolesArea, 'm_eng_f', 'C_d', 'rho_f', 'p_loss_inj', 'p_cc')),
    'A_th_ox':UnknownVariable("Area di tutti i fori piastra ossidante",'m^2', CalcFunction(calcTotalHolesArea, 'm_eng_ox', 'C_d', 'rho_ox', 'p_loss_inj', 'p_cc')),
    'n_h_f':UnknownVariable("Numero di fori piastra combustibile di diametro 1mm",'-', CalcFunction(calcNumber1Holes, 'A_th_f')),
    'n_h_ox':UnknownVariable("Numero di fori piastra ossidante di diametro 1mm",'-', CalcFunction(calcNumber1Holes, 'A_th_ox')),
    'n_h':UnknownVariable("Numero di fori di ciascunna linea",'-', CalcFunction(calcNumberHoles, 'n_h_f', 'n_h_ox')),
    'A_1h_f':UnknownVariable("Area di un foro-combustibile",'m^2', CalcFunction(calcHoleArea, 'A_th_f', 'n_h')),
    'A_1h_ox':UnknownVariable("Area di un foro-ossidante",'m^2', CalcFunction(calcHoleArea, 'A_th_ox', 'n_h')),
    'D_1h_f':UnknownVariable("Diametro di un foro-combustibile",'m', CalcFunction(calcDiameter, 'A_1h_f')),
    'D_1h_ox':UnknownVariable("Diametro di un foro-ossidante",'m', CalcFunction(calcDiameter, 'A_1h_ox')),
    'u_f':UnknownVariable("Velocità iniezione combustibile",'m/s', CalcFunction(calcInjectionVelocity, 'C_d', 'p_loss_inj', 'p_cc', 'rho_f')),
    'u_ox':UnknownVariable("Velocità iniezione ossidante",'m/s', CalcFunction(calcInjectionVelocity, 'C_d', 'p_loss_inj', 'p_cc', 'rho_ox')),
    'alpha_f':UnknownVariable("Inclinazione linea iniezione combustibile",'rad', CalcFunction(calcFuelInjectionAngle, 'm_eng_ox', 'm_eng_f', 'u_ox', 'u_f', 'alpha_ox')),
}

feed_system_constants={
    'p_loss_inj':InputVariable("Frazione perdite di carico piastra di iniezione",'-',0.2),
    'p_loss_exc':InputVariable("Frazione perdite di carico scambiatore di calore",'-',0.15),
    'p_loss_feed':InputVariable("Frazione perdite di carico linee di alimentazione",'-',0.1),
    'p_loss_valves':InputVariable("Frazione perdite di carico valvole",'-',0.15),
    'r_pb':InputVariable("Rapporto massico di miscela preburner",'-',1),
    'eta_pump_f':UnknownVariable("Rendimento della pompa di combustibile",'-',CalcFunction(lambda fName: 0.75 if fName=='LH2' else 0.8, 'fuelName')),
    'eta_pump_ox':InputVariable("Rendimento della pompa di ossidante",'-',0.8),
    'eta_mt':InputVariable("Rendimento meccanico della turbina",'-',0.975), #delft thesis,
    'eta_ad':InputVariable("Rendimento adiabatico della turbina",'-',0.7), #delft thesis
    'beta_t':InputVariable("Rapporto di compressione turbina",'-',20), #delft thesis
    'p_out_pb':UnknownVariable("Pressione di uscita turbina",'Pa',CalcFunction(lambda pc,beta: pc/beta ,'p_pb', 'beta_t'))
    #'p_out_pb':InputVariable("Pressione di uscita turbina",'Pa',10000), #non lo so, dobbiamo capire
}

preburner={
    'cp_pb':UnknownVariable("C_p preburner",'J/(kg*K)',CalcFunction(getCeaChamberCp,'pb_cea','p_pb','r_pb')),
    'T_pb':UnknownVariable("Temperatura preburner",'K',CalcFunction(getCeaChamberTemperature,'pb_cea','p_pb','r_pb')),
    'y_pb':UnknownVariable("Rapporto calori specifici preburner",'-',CalcFunction(getCeaThroatGam,'pb_cea','p_pb','r_pb')),
}

feed_system_variables={
    'm_eng_f':UnknownVariable("Portata massica di combustibile al motore",'kg/s',CalcFunction(calcFuelRate,'m_p','r_cc')),
    'm_eng_ox':UnknownVariable("Portata massica di ossidante al motore", 'kg/s',CalcFunction(calcOxidizerRate, 'm_eng_f', 'r_cc')),
    'pstar_f':UnknownVariable("Pressione combustibile a valle della pompa",'Pa',CalcFunction(calcPStarF,'p_cc','p_loss_inj','p_loss_exc','p_loss_feed','p_loss_valves')),
    'pstar_ox':UnknownVariable("Pressione ossidante a valle della pompa",'Pa',CalcFunction(calcPStarOx,'p_cc','p_loss_inj','p_loss_feed','p_loss_valves')),
    'deltap_pump_f':UnknownVariable("Delta P pompa combustibile",'Pa',CalcFunction(lambda pstar,ptank: pstar-ptank,'pstar_f','p_tank_f')),
    'deltap_pump_ox':UnknownVariable("Delta P pompa ossidante",'Pa',CalcFunction(lambda pstar,ptank: pstar-ptank,'pstar_ox','p_tank_ox')),
    'q_eng_f':UnknownVariable("Portata volumetrica di combustibile al motore",'m^3/s',CalcFunction(lambda m,rho: m/rho,'m_eng_f','rho_f')),
    'q_eng_ox':UnknownVariable("Portata volumetrica di ossidante al motore",'m^3/s',CalcFunction(lambda m,rho: m/rho,'m_eng_ox','rho_ox')),
    'q_spil_f':UnknownVariable("Portata volumetrica di combustibile spillato",'m^3/s',CalcFunction(calcSpilF,'q_eng_f','deltap_pump_f','deltap_pump_ox','eta_pump_f','eta_pump_ox','rho_f','rho_ox','r_cc','r_pb','eta_mt','eta_ad','cp_pb','T_pb','p_out_pb','p_pb','y_pb')),
    'q_tot_f':UnknownVariable("Portata volumetrica totale di combustibile",'m^3/s',CalcFunction(lambda qsp,qeng: qsp+qeng,'q_spil_f','q_eng_f')),
    'q_spil_ox':UnknownVariable("Portata volumetrica di ossidante spillato",'m^3/s',CalcFunction(lambda qspf,tau,rhof,rhoox: qspf*tau*rhof/rhoox,'q_spil_f','r_pb','rho_f','rho_ox')),
    'q_tot_ox':UnknownVariable("Portata volumetrica totale di ossidante",'m^3/s',CalcFunction(lambda qsp,qeng: qsp+qeng,'q_spil_ox','q_eng_ox')),
    'm_spil_f':UnknownVariable("Portata massica di combustibile spillata",'kg/s',CalcFunction(lambda q,rho: q*rho,'q_spil_f','rho_f')),
    'm_spil_ox':UnknownVariable("Portata massica di ossidante spillata",'kg/s',CalcFunction(lambda q,rho: q*rho,'q_spil_ox','rho_ox')),
    'm_tot_f':UnknownVariable("Portata massica di combustibile totale",'kg/s',CalcFunction(lambda q,rho: q*rho,'q_tot_f','rho_f')),
    'm_tot_ox':UnknownVariable("Portata massica di ossidante totale",'kg/s',CalcFunction(lambda q,rho: q*rho,'q_tot_ox','rho_ox')),
    'W_pump_f':UnknownVariable("Potenza richiesta dalla pompa di combustibile",'W',CalcFunction(lambda q,p,eta: q*p/eta,'q_tot_f','deltap_pump_f','eta_pump_f')),
    'W_pump_ox':UnknownVariable("Potenza richiesta dalla pompa di ossidante",'W',CalcFunction(lambda q,p,eta: q*p/eta,'q_tot_ox','deltap_pump_ox','eta_pump_ox')),
}

static_propulsive_parameters={
    'Is_n':UnknownVariable("Impulso specifico nominale",'s',CalcFunction(calcSpecificImpulse,'thr_n','m_p','g_0')),
    'thr_ad':UnknownVariable("Spinta a quota di adattamento",'N',CalcFunction(calcThrust,'m_p','u_e','A_e','p_e', 'p_e')),
    'z_ad':UnknownVariable("Quota di adattamento",'m',CalcFunction(calcAltitudeFromPressure,'p_e','p_0','T_0','a','g_0','R_air')),
    'thr_n':UnknownVariable("Spinta nominale",'N',CalcFunction(kiloNewtonToNewton,'T_n')),
    'Is_ad':UnknownVariable("Impulso specifico a quota di adattamento",'s',CalcFunction(calcAdaptedSpecificImpulse,'u_e','g_0')),
    'ct_ad':UnknownVariable("Coefficiente di spinta a quota di adattamento",'-',CalcFunction(calcAdaptedThrustCoefficient,'eta_2D','Is_ad','g_0','c_star')),
    'ct_n':UnknownVariable("Coefficiente di spinta nominale",'-',CalcFunction(calcThrustCoefficient,'p_n', 'y_cc_e', 'eps', 'p_e', 'p_cc')),
    'ct_vac':UnknownVariable("Coefficiente di spinta nel vuoto",'-',CalcFunction(calcThrustCoefficient,'p_vac', 'y_cc_e', 'eps', 'p_e', 'p_cc')),
    'Is_vac':UnknownVariable("Impulso specifico nel vuoto",'s',CalcFunction(calcSpecificImpulse,'thr_vac','m_p','g_0')),
    'Iv_vac':UnknownVariable("Impulso specifico volumetrico nel vuoto",'s*kg/m^3', CalcFunction(calcVolumetricSpecificImpulse, 'Is_vac', 'rho_avg')),
    'Itot_vac':UnknownVariable("Impulso specifico totale nel vuoto",'N*s', CalcFunction(calcTotalVolumetricImpulse, 'Is_vac', 'M_ox', 'M_f', 'g_0')),
    'thr_vac':UnknownVariable("Spinta nel vuoto",'N',CalcFunction(calcThrust,'m_p','u_e','A_e','p_e', 'p_vac'))
}

nonstatic_propulsive_parameters={
    #ANALYTICAL VALUES
    'ct_var':UnknownVariable("Coefficiente di spinta",'-',CalcFunction(calcThrustCoefficient,'p','y_cc_e','eps','p_e','p_cc')),
    'thr_var':UnknownVariable("Spinta",'N',CalcFunction(calcThrust,'m_p','u_e','A_e','p_e', 'p')),
    'I_s':UnknownVariable("Impulso specifico",'s', CalcFunction(calcSpecificImpulse, 'thr_var', 'm_p', 'g_0')),
    'I_v':UnknownVariable("Impulso specifico volumetrico",'s*kg/m^3', CalcFunction(calcVolumetricSpecificImpulse, 'I_s', 'rho_avg')),
    'I_tot':UnknownVariable("Impulso specifico totale",'N*s', CalcFunction(calcTotalVolumetricImpulse, 'I_s', 'M_ox', 'M_f', 'g_0')),

    #CEA VALUES
    #'ct_var':UnknownVariable("Coefficiente di spinta",'-',CalcFunction(getCeaThrustCoefficient, 'cc_cea', 'p', 'p_cc', 'r_cc', 'eps',iter=True)),
    #'thr_var':UnknownVariable("Spinta",'N',CalcFunction(calcThrust,'m_p','u_e','A_e','p_e', 'p')),
    #'I_s':UnknownVariable("Impulso specifico",'s', CalcFunction(getCeaSpecificImpulse, 'cc_cea', 'p_cc', 'r_cc', 'eps', 'p',iter=True)),
    #'I_v':UnknownVariable("Impulso specifico volumetrico",'s*kg/m^3', CalcFunction(calcVolumetricSpecificImpulse, 'I_s', 'rho_avg')),
    #'I_tot':UnknownVariable("Impulso specifico totale",'N*s', CalcFunction(calcTotalVolumetricImpulse, 'I_s', 'M_ox', 'M_f', 'g_0')),
}

nozzle={
    'theta':InputVariable("Half expansion angle",'rad', np.pi/12),#CAPIRE SE È DATO GLOBALE O RELATIVO AL SINGOLO STADIO. SE RELATIVO, ALLORA AGGIUNGI SU GOOGLE SPREADSHEET
    'A_t':UnknownVariable("Sezione di gola",'m^2',CalcFunction(calcThroatArea,'m_p','u_e','p_cc','ct_n')),
    'D_t':UnknownVariable("Diametro di gola",'m',CalcFunction(calcDiameter,'A_t')),
    'A_e':UnknownVariable("Area di efflusso",'m^2',CalcFunction(calcExitArea,'eps','A_t')),
    'D_e':UnknownVariable("Diametro di efflusso",'m',CalcFunction(calcDiameter,'A_e')),
    'L_cone':UnknownVariable("Lunghezza cono",'m', CalcFunction(calcConeLength, 'eps', 'D_t', 'theta')),
    'L_bell':UnknownVariable("Lunghezza campana",'m', CalcFunction(calcBellLength, 'L_cone')),#CALCOLATA ALL'80% DI L_cone
    #'theta_i':UnknownVariable("Angolo iniziale tratto convergente",'rad', CalcFunction(calcThetai, 'D_c', 'D_t')),
    #'theta_i':UnknownVariable("Angolo iniziale tratto convergente",'rad', CalcFunction(lambda x:-2*np.pi+x,'alpha')),
    'x_conv':UnknownVariable("Tratto convergente ugello-x",'m', CalcFunction(calcXConv, 'alpha', 'D_t')),
    #Array contenente coordinate x dei punti della funzione, il cui grafico disegna il tratto convergente dell'ugello
    'y_conv':UnknownVariable("Tratto convergente ugello-y",'m', CalcFunction(calcYConv, 'alpha', 'D_t')),
    #Array contenente coordinate y dei punti della funzione, il cui grafico disegna il tratto convergente dell'ugello
    'x_div_plus':UnknownVariable("Tratto divergente + ugello-x",'m', CalcFunction(calcXDivPlus, 'theta_n', 'D_t')),
    #Array contenente coordinate x dei punti della funzione, il cui grafico disegna il tratto divergente a concavità verso l'alto dell'ugello
    'y_div_plus':UnknownVariable("Tratto divergente + ugello-y",'m', CalcFunction(calcYDivPlus,'theta_n', 'D_t')),
    #Array contenente coordinate y dei punti della funzione, il cui grafico disegna il tratto divergente a concavità verso l'alto dell'ugello
    'x_div_minus':UnknownVariable("Tratto divergente - ugello-x",'m', CalcFunction(calcXDivMinus, 'theta_n', 'theta_e', 'D_t', 'L_bell', 'D_e')),
    #Array contenente coordinate x dei punti della funzione, il cui grafico disegna il tratto divergente a concavità verso il basso dell'ugello
    'y_div_minus':UnknownVariable("Tratto divergente - ugello-y",'m', CalcFunction(calcYDivMinus, 'theta_n', 'theta_e', 'D_t', 'L_bell', 'D_e')),
    #Array contenente coordinate y dei punti della funzione, il cui grafico disegna il tratto divergente a concavità verso il basso dell'ugello

    #Raccordo con la camera di combustione
    'rad_lim':InputVariable("Raggio di curvatura minimo possibile",'m',0),
    'rad_min':UnknownVariable("Raggio di curvatura minimo desiderato",'m',CalcFunction(lambda x: x/4,'D_c')),
    'alpha_lim':UnknownVariable("Limite alpha raccordo",'rad',CalcFunction(calcAlpha,'D_c','D_t','rad_lim')),
    'alpha_radmin':UnknownVariable("Alpha corrispondente a raggio di curvatura minimo",'rad',CalcFunction(calcAlpha,'D_c','D_t','rad_min')),
    'alpha_min':InputVariable("Alpha minimo desiderato",'rad',(360-135)*np.pi/180),
    'alpha':UnknownVariable("Alpha",'rad',CalcFunction(lambda *x: np.amax(x),'alpha_lim','alpha_min','alpha_radmin')),

    'l_tc':UnknownVariable("Distanza gola-cc",'m',CalcFunction(calcLTC,'D_c','D_t','alpha')),
    'rad_rac':UnknownVariable("Raggio di curvatura raccordo",'m',CalcFunction(calcRad,'D_c','D_t','alpha')),

    'x_rac':UnknownVariable("Tratto di raccordo convergente-x",'m', CalcFunction(calcXRac, 'alpha', 'l_tc', 'rad_rac')),
    'y_rac':UnknownVariable("Tratto di raccordo convergente-y",'m', CalcFunction(calcYRac, 'alpha', 'D_c', 'rad_rac')),

    'x_cc':UnknownVariable("X camera di combustione",'m',CalcFunction(calcXCc,'l_tc','L_c')),
    'y_cc':UnknownVariable("Y camera di combustione",'m',CalcFunction(calcYCc,'D_c')),
}

tanks={
    'M_f':UnknownVariable("Massa di combustibile",'kg', CalcFunction(calcMass, 'm_eng_f', 't_b', 'k_s')),
    'M_ox':UnknownVariable("Massa di ossidante",'kg', CalcFunction(calcMass, 'm_eng_ox', 't_b', 'k_s')),
    'V_f':UnknownVariable("Volume di combustibile",'m^3', CalcFunction(calcVolume, 'M_f', 'rho_f')),
    'V_ox':UnknownVariable("Volume di ossidante",'m^3', CalcFunction(calcVolume, 'M_ox', 'rho_ox')),
    'rho_avg':UnknownVariable("Densità media propellente",'kg/m^3', CalcFunction(calcRhoAvg, 'M_f', 'M_ox', 'V_f', 'V_ox')),
    'k_s':InputVariable("Coefficiente di sicurezza massa",'-', 1.05),
}

misc={
    'Ltot':UnknownVariable("Lunghezza totale motore",'m',CalcFunction(lambda lc,conv,div: lc+(div[-1]-conv[0]) ,'L_c','x_conv','x_div_minus')),
}
