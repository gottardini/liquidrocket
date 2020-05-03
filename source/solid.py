from models import *
from source.functions import *
import numpy as np

###TODO
prop={
    'thr_n':UnknownVariable("Spinta nominale",'N',CalcFunction(kiloNewtonToNewton,'T_n')),
    'm_p':UnknownVariable("Portata massica",'kg/s',CalcFunction(lambda t,i_s,g : t/(i_s*g),'thr_n','Is_vac','g_0')),
    'thr_var':UnknownVariable("Spinta in funzione della quota",'N',CalcFunction(lambda i_s,g,m : i_s*g*m, 'I_s','g_0','m_p')),
    'I_s':UnknownVariable("Impulso specifico",'s',CalcFunction(lambda issl,isvac,pssl,p: issl+(isvac-issl)/pssl*(pssl-p),'Is_sl','Is_vac','p_0','p')),
}

atmoshpere={
    'p':UnknownVariable("Pressione atmosferica",'Pa',CalcFunction(calcPressureFromAltitude,'z','p_0','T_0','a','g_0','R_air')),
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
