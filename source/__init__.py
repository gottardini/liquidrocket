from models import *
from source.functions import *

constants={
    "R_u":InputVariable("Costante dei gas ideali [J/(mol*K)]", 8.31446261815324),
    "g_0":InputVariable("Accelerazione gravitzionale a quota zero [m/s^2]", 9.807),
    "a":InputVariable("Gradiente di temperatura verticale [K/m]",0.0065),
    "p_0":InputVariable("Pressione a quota zero [Pa]", 101325),
    "T_0":InputVariable("Temperatura a quota zero [K]", 288.16),
    "GUESS":InputVariable("Stima pressione all'efflusso",15000)
}

variables={
    "R_cp":UnknownVariable("Costante dei gas di scarico",CalcFunction(calcGasConstant,'R_u','Mm_cp')),
    "GAMMA":UnknownVariable("Funzione di Van Kerckhove",CalcFunction(vanker,'y_c')),
    "p_e":UnknownVariable("Pressione all'efflusso",CalcFunction(calcExitPressure,'y_c','p_c','eps','GUESS')),
    "c_star":UnknownVariable("Velocità caratteristica",CalcFunction(calcCharacteristicVelocity,'R_cp','T_c','GAMMA')),
    "u_e":UnknownVariable("Velocità all'efflusso",CalcFunction(calcExitVelocity,'eta_2D','y_c','R_cp','T_c','p_e','p_c')),
    "I_s_e":UnknownVariable("Impulso specifico a quota zero",CalcFunction(calcSpecificImpulse,'u_e','g_0')),
    "c_t_e":UnknownVariable("Coefficiente di spinta a quota zero",CalcFunction(calcThrustCoefficient,'eta_2D','I_s_e','g_0','c_star'))
}

#outputs=["c_star","I_s_e"]
outputs=[key for key,val in variables.items()]
