import matplotlib.pyplot as plt
from collections import OrderedDict
import numpy as np

class PostProcesser:
    def __init__(self,rockets):
        self.rockets=rockets

        """
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
        """

    ###THIS IS ABOUT TO GET MESSY AND NOT FLEXIBLE, BUT I HAVE NO TIME TO MAKE IT BTFL
    def make(self):
        ###THRUST-Z
        figThrust_z, axThrust_z = plt.subplots(figsize=(8, 8),num="Spinta in funzione della quota")
        axThrust_z.set_xlabel("Quota [m]")
        axThrust_z.set_ylabel("Spinta [N]")

        ###ISP-Z
        figIsp_z, axIsp_z = plt.subplots(figsize=(8, 8),num="Impulso specifico in funzione della quota")
        axIsp_z.set_xlabel("Quota [m]")
        axIsp_z.set_ylabel("Impulso specifico [s]")

        for rocketName, rocket in self.rockets.items():
            ###THRUST-Z
            sep_figThrust_z, sep_axThrust_z = plt.subplots(figsize=(8, 8),num="Spinta in funzione della quota - %s"%(rocketName))
            sep_axThrust_z.set_xlabel("Quota [m]")
            sep_axThrust_z.set_ylabel("Spinta [N]")

            ###ISP-Z
            sep_figIsp_z, sep_axIsp_z = plt.subplots(figsize=(8, 8),num="Impulso specifico in funzione della quota- %s"%(rocketName))
            sep_axIsp_z.set_xlabel("Quota [m]")
            sep_axIsp_z.set_ylabel("Impulso specifico [s]")

            for blockIndex in range(len(rocket)):
                block=rocket[blockIndex]
                blockSolved=block['solvedData']

                ###THRUST-Z
                sep_axThrust_z.plot(blockSolved['z'].getValue(),blockSolved['thr_var'].getValue()*block['qty'],label=block['name'])
                sep_axThrust_z.legend()
                sep_axThrust_z.set_yscale('log')
                sep_axThrust_z.grid(True, which="both")
                sep_axThrust_z.set_title("Contributo spinta dei vari stadi - "+rocketName)

                ###THRUST-Z
                sep_axIsp_z.plot(blockSolved['z'].getValue(),blockSolved['I_s'].getValue(),label=block['name'])
                sep_axIsp_z.legend()
                sep_axIsp_z.set_yscale('linear')
                sep_axIsp_z.grid(True, which="both")
                sep_axIsp_z.set_title("Impulso specifico dei vari stadi - "+rocketName)
