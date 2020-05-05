import numpy as np

"""
"rockets" object is a dictionary of lists:
{
"Ariane V ECA": [...],
"Falcon Heavy": [...],
"Saturn V": [...]
}
The exact key names are defined in config.py

Each list is a list of "blocks", where a "block" is a group of engines of the same kind working within the same timespan

Each block is a dictionary defined as follows:
{
'name': "<stage name>",
'index': <engine index>,
'qty': <engines quantity>,
'type': '<engine type>',
'tStart': <ignition time>,
'tEnd': <cut-off time>,
'zStart': <ignition altitude>,
'zEnd': <cut-off altitude>,
'engName': "<engine name>"
'solvedData': <data dictionary of the solved model>
}

The "solved data dictionary" is just the big dictionary with every imaginable variable of the model

"""

tables={
    "Parametri propulsivi calcolati analiticamente":(['Is_vac', 'Iv_vac', 'Itot_vac', 'u_e', 'ct_vac', 'c_star', 'thr_vac'],
    ["Vulcain II","HM7B","Merlin 1D+","Merlin 1D+ vac","F-1","J-2 (II° stadio)"]),
    #"Parametri propulsivi calcolati tramite CEA":(['Is_vac', 'Iv_vac', 'Itot_vac', 'u_e', 'ct_vac', 'c_star', 'thr_vac'],
    #["Vulcain II","HM7B","Merlin 1D+","Merlin 1D+ vac","F-1","J-2 (II° stadio)"]),
    "Grandezze tipiche motore":(['m_eng_f', 'm_eng_ox', 'm_p', 'M_f', 'M_ox', 'D_e', 'D_t', 'T_cc', 'D_c', 'L_c', 'W_pump_f', 'W_pump_ox', 'L_bell'],
    ["Vulcain II","HM7B","Merlin 1D+","Merlin 1D+ vac","F-1","J-2 (II° stadio)"]),
}
aliases={
    "J-2 (II° stadio)":"J-2"
}

class Latexer:
    def __init__(self,rockets):
        self.rockets=rockets

    def make(self):
        output = ""
        engines = {}
        for rocketName, rocketData in self.rockets.items():
            for block in rocketData:
                if block['engName'] not in engines:
                    engines[block['engName']]=block['solvedData']

        for tableName,tableValues in tables.items():
            names = []
            for name in tableValues[1]:
                if name in aliases:
                    names.append(aliases[name])
                else:
                    names.append(name)
            output += (tableName.upper() +  "\n\n"
            "\\begin{center}"
            "\\begin{tabular}{*{"+ str(len(tableValues[1])+2) +"}{|c}|} \n"
            "\\hline \n"
            "\\multicolumn{"+ str(len(tableValues[1])+2) +"}{|c|}{"+ tableName +"} \\\\ \n"
            "\\hline \n"
            "Variabile & Unità di misura & " + ' & '.join(names) +"\\\\ \n")
            for i in np.arange(len(tableValues[0])):
                values = [list(engines.items())[0][1][tableValues[0][i]].units]
                values += ['{:.2f}'.format(engines[engName][tableValues[0][i]].getValue()[0]) for engName in tableValues[1]]
                output += "\\hline \n$" + tableValues[0][i].replace('_', '\_') + '$ & ' + ' & '.join(values) + "\\\\ \n"
            output += (" \\hline \n"
            "\\end{tabular}"
            "\\end{center} \n\n")

        f = open("out/latex/latex_tables.txt", 'w+')
        f.write(output)
        f.close()
