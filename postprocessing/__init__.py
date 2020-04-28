import matplotlib.pyplot as plt
from collections import OrderedDict
import numpy as np

class PostProcesser:
    def __init__(self,rockets):
        self.rockets=rockets

        ###GRAFICI
        self.figures=OrderedDict({
            "Pressione in funzione della quota":['z',['p','p_tropo','p_e']],
            "Spinta in funzione della pressione":['p',['thr_var','thr_n','thr_ad']],
            "Spinta in funzione della quota":['z',['thr_var','thr_n','thr_ad']],
            })

        self.styles=[
            [{"color":"black"},{"color":"gray"},{"color":"green","linestyle":"--"}],
            [{"color":"blue"},{"color":"gray","linestyle":"--"},{"color":"green","linestyle":"--"}],
            [{"color":"blue"},{"color":"gray","linestyle":"--"},{"color":"green","linestyle":"--"}],
        ]

        self.markers=[
            [{"data":"z_ad","params":{"color":"gray","linestyle":"--","linewidth":1}}],
            [{"data":"p_e","params":{"color":"gray","linestyle":"--","linewidth":1}}],
            [{"data":"z_ad","params":{"color":"gray","linestyle":"--","linewidth":1}}],
        ]

        self.labels=[
            ("Quota [m]","Pressione [Pa]"),
            ("Pressione [Pa]","Spinta [N]"),
            ("Quota [m]","Spinta [N]"),
        ]

    def make(self):
        pass
