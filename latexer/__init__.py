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

class Latexer:
    def __init__(self,rockets):
        self.rockets=rockets

    def make(self):
        pass
