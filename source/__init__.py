from models import *
from source.functions import *
import numpy as np

variables_array={
    "p":InputVariable("Quota",np.linspace(101325,0,num=50))
}

constants={
    "R_u":InputVariable("Costante dei gas ideali [J/(mol*K)]", 8.31446261815324),
    "g_0":InputVariable("Accelerazione gravitzionale a quota zero [m/s^2]", 9.807),
    "a":InputVariable("Gradiente di temperatura verticale [K/m]",0.0065),
    "p_0":InputVariable("Pressione a quota zero [Pa]", 101325),
    "T_0":InputVariable("Temperatura a quota zero [K]", 288.16),
    "GUESS":InputVariable("Stima pressione all'efflusso",50000)
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
    "Is_ad":UnknownVariable("Impulso specifico a quota di adattamento",CalcFunction(calcAdaptedSpecificImpulse,'u_e','g_0')),
    "ct_ad":UnknownVariable("Coefficiente di spinta a quota di adattamento",CalcFunction(calcAdaptedThrustCoefficient,'eta_2D','Is_ad','g_0','c_star')),
    "ct_n":UnknownVariable("Coefficiente di spinta nominale",CalcFunction(calcThrustCoefficient,'p_n', 'y_c', 'eps', 'p_e', 'p_c')),
    "m_p":UnknownVariable("Portata massica di propellente",CalcFunction(calcPropFlowRate,'T_n','u_e','eps','p_c','ct_n','p_e','p_n')),
    "A_t":UnknownVariable("Sezione di gola",CalcFunction(calcThroatArea,'m_p','u_e','p_c','ct_n')),
    "D_t":UnknownVariable("Diametro di gola",CalcFunction(calcThroatDiameter,'A_t')),
    "A_e":UnknownVariable("Area di efflusso",CalcFunction(calcExitArea,'eps','A_t')),
    "D_e":UnknownVariable("Diametro di efflusso",CalcFunction(calcExitDiameter,'A_e')),
}

variables_var={
    "ct_var":UnknownVariable("Coefficiente di spinta in funzione della pressione",CalcFunction(calcThrustCoefficient,'p','y_c','eps','p_e','p_c')),
    "thr":UnknownVariable("Spinta in funzione della pressione",CalcFunction(calcThrust,'m_p','u_e','A_e','p_e', 'p'))
}

variables={**variables_gas,**variables_fluid,**variables_static,**variables_array,**variables_var}
