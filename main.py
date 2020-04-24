import sys
import utils
import config
print(utils.getLogo())
from solver import Solver
from models import InputVariable, UnknownVariable
from grapher import Grapher
from postprocessing import PostProcesser
from loader import DataLoader
import time
import matplotlib.pyplot as plt
import traceback
import argparse
import pprint
import logging
from colorlog import ColoredFormatter
LOGFORMAT = "  %(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Liquid rocket solver.')
    parser.add_argument('--graph', dest='graph', action='store_true')
    parser.add_argument('--debug', dest='debug', action='store_true')
    parser.add_argument('--all', dest='all', action='store_true')
    parser.add_argument('--postproc', dest='postproc', action='store_true')
    parser.set_defaults(graph=False)
    parser.set_defaults(debug=False)
    parser.set_defaults(all=False)
    parser.set_defaults(postproc=False)
    args = parser.parse_args()

    ###SOME SETUP
    pp=pprint.PrettyPrinter()
    LOG_LEVEL = logging.DEBUG if args.debug else logging.INFO
    logging.root.setLevel(LOG_LEVEL)
    formatter = ColoredFormatter(LOGFORMAT)
    stream = logging.StreamHandler()
    stream.setLevel(LOG_LEVEL)
    stream.setFormatter(formatter)
    logger = logging.getLogger('pythonConfig')
    logger.setLevel(LOG_LEVEL)
    logger.addHandler(stream)

    ###BEGINNING OF THE ACTUAL PROBLEM
    loader=DataLoader(config.datafile)
    inputData=loader.load()
    #pp.pprint(inputData)
    rocketModels=config.rockets.copy()
    for rocketName,rocketData in rocketModels.items():
        for blockIndex in range(len(rocketData)):
            engineName,engineData=utils.getEngineData(inputData, rocketData[blockIndex]['index'])
            unsolvedModel=utils.getUnsolvedModel()
            #INJECT SPECIFIC STAGE DATA
            unsolvedModel['t_b']=InputVariable("Tempo di combustione",rocketData[blockIndex]['tEnd']-rocketData[blockIndex]['tStart'])
            ###
            modelData=utils.mergeData([engineData,unsolvedModel])
            task=[key for key,val in modelData.items() if isinstance(val,UnknownVariable)]

            pp.pprint(modelData)
            #LET'S SOLVE
            grph=Grapher(view=args.graph,debug=args.debug,cool=False)
            slvr=Solver(modelData,task,grph,logger)
            utils.tic()
            try:
                if slvr.validateTree():
                    logger.info("Tree building took %s seconds"%(utils.toc()))
                    logger.info("Solving tree...")
                    utils.tic()
                    res=slvr.solve()
                    logger.info("Done! Solving took %s seconds."%(utils.toc()))
                    logger.debug(res)
                    logger.debug("\n"+pp.pformat({key:val.getValue() for key,val in slvr.data.items()}))
                    rocketModels[rocketName][blockIndex]['solvedData']=slvr.data.copy()
            except Exception:
                 print(traceback.format_exc())
            plt.show()
    plt.show()
