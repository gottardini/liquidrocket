from models import *
from source.functions import *
import numpy as np

variables_array={
    "z":InputVariable("Quota [m]",np.linspace(0,1e5,50)),
}

constants={
    "R_u":InputVariable("Costante dei gas ideali", 8.31446261815324), # [J/(mol*K)]
    "g_0":InputVariable("Accelerazione gravitzionale a quota zero", 9.807), # [m/s^2]
    "a":InputVariable("Gradiente di temperatura verticale",0.0065), # [K/m]
    "p_0":InputVariable("Pressione a quota zero", 101325), # [Pa]
    "T_0":InputVariable("Temperatura a quota zero", 288.16), # [K]
    "GUESS":InputVariable("Stima pressione all'efflusso",20000),
    "R_air":InputVariable("Costante specifica dell'aria",287.058)
}

variables_gas={
    "R_cp":UnknownVariable("Costante dei gas di scarico",CalcFunction(calcGasConstant,'R_u','Mm_cp')),
    "GAMMA":UnknownVariable("Funzione di Van Kerckhove",CalcFunction(vanker,'y_c'))
}

variables_fluid={
    "p_e":UnknownVariable("Pressione all'efflusso",CalcFunction(calcExitPressure,'y_c','p_c','eps','GUESS')),
    "u_e":UnknownVariable("Velocità all'efflusso",CalcFunction(calcExitVelocity,'eta_2D','y_c','R_cp','T_c','p_e','p_c')),
    "c_star":UnknownVariable("Velocità caratteristica",CalcFunction(calcCharacteristicVelocity,'R_cp','T_c','GAMMA')),
}

variables_static={
    "thr_ad":UnknownVariable("Spinta a quota di adattamento",CalcFunction(calcThrust,'m_p','u_e','A_e','p_e', 'p_e')),
    "z_ad":UnknownVariable("Quota di adattamento",CalcFunction(calcAltitudeFromPressure,'p_e','p_0','T_0','a','g_0','R_air')),
    "thr_n":UnknownVariable("Spinta nominale",CalcFunction(kiloNewtonToNewton,'T_n')),
    "Is_ad":UnknownVariable("Impulso specifico a quota di adattamento",CalcFunction(calcAdaptedSpecificImpulse,'u_e','g_0')),
    "ct_ad":UnknownVariable("Coefficiente di spinta a quota di adattamento",CalcFunction(calcAdaptedThrustCoefficient,'eta_2D','Is_ad','g_0','c_star')),
    "ct_n":UnknownVariable("Coefficiente di spinta nominale",CalcFunction(calcThrustCoefficient,'p_n', 'y_c', 'eps', 'p_e', 'p_c')),
    "m_p":UnknownVariable("Portata massica di propellente",CalcFunction(calcPropFlowRate,'thr_n','u_e','eps','p_c','ct_n','p_e','p_n')),
    "A_t":UnknownVariable("Sezione di gola",CalcFunction(calcThroatArea,'m_p','u_e','p_c','ct_n')),
    "D_t":UnknownVariable("Diametro di gola",CalcFunction(calcThroatDiameter,'A_t')),
    "A_e":UnknownVariable("Area di efflusso",CalcFunction(calcExitArea,'eps','A_t')),
    "D_e":UnknownVariable("Diametro di efflusso",CalcFunction(calcExitDiameter,'A_e')),
    "m_f":UnknownVariable("Portata massica di combustibile",CalcFunction(calcFuelRate,'m_p','r'))
}


variables_var={
    "p":UnknownVariable("Pressione atmosferica",CalcFunction(calcPressureFromAltitude,'z','p_0','T_0','a','g_0','R_air')),
    "p_tropo":UnknownVariable("Pressione troposferica",CalcFunction(calcTropoPressure,'z','p_0','T_0','a','g_0','R_air')),
    "ct_var":UnknownVariable("Coefficiente di spinta",CalcFunction(calcThrustCoefficient,'p','y_c','eps','p_e','p_c')),
    "thr_var":UnknownVariable("Spinta",CalcFunction(calcThrust,'m_p','u_e','A_e','p_e', 'p')),

}

variables={**variables_gas,**variables_fluid,**variables_static,**variables_array,**variables_var}
