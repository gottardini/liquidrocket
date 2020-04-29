from models import *
from source.functions import *
import numpy as np

###TODO
prop={
    'thr_n':UnknownVariable("Spinta nominale",'N',CalcFunction(kiloNewtonToNewton,'T_n')),
    'thr_var':UnknownVariable("Spinta in funzione della quota",'N',CalcFunction(lambda z,t: np.full(len(z),t), 'z','thr_n'))
}
