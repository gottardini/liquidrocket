import sys
import utils
import config
from solver import Solver
from models import InputVariable, UnknownVariable
from grapher import Grapher
from postprocessing import PostProcesser
from loader import DataLoader
from latexer import Latexer
from comparer import Comparer
from nozzleplotter import NozzlePlotter
from outputcea import OutputCea
import time
import matplotlib.pyplot as plt
import traceback
import argparse
import pprint
import logging
import numpy as np
import copy
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
    parser.add_argument('--job', dest='all', action='store_false')
    parser.add_argument('--postproc', dest='postproc', action='store_true')
    parser.add_argument('--cool', dest='cool', action='store_true')
    parser.add_argument('--labels', dest='labels', action='store_true')
    parser.add_argument('--latex', dest='latex', action='store_true')
    parser.add_argument('--logs', dest='logs', action='store_true')
    parser.add_argument('--compare', dest='compare', action='store_true')
    parser.add_argument('--nozzleplot', dest='nozzleplot', action='store_true')
    parser.add_argument('--nooutput', dest='nooutput', action='store_true')
    parser.add_argument('--noshow', dest='noshow', action='store_true')
    parser.add_argument('--outputcea', dest='outputcea', action='store_true')
    parser.set_defaults(graph=False)
    parser.set_defaults(debug=False)
    parser.set_defaults(all=True)
    parser.set_defaults(postproc=False)
    parser.set_defaults(cool=False)
    parser.set_defaults(labels=False)
    parser.set_defaults(latex=False)
    parser.set_defaults(logs=False)
    parser.set_defaults(compare=False)
    parser.set_defaults(nozzleplot=False)
    parser.set_defaults(nooutput=False)
    parser.set_defaults(noshow=False)
    parser.set_defaults(outputcea=False)
    args = parser.parse_args()

    ###SOME SETUP
    pp=pprint.PrettyPrinter()
    LOG_LEVEL = logging.ERROR if args.nooutput else (logging.DEBUG if args.debug else logging.INFO)
    logging.root.setLevel(LOG_LEVEL)

    formatter = ColoredFormatter(LOGFORMAT)
    stream = logging.StreamHandler()
    stream.setLevel(LOG_LEVEL)
    stream.setFormatter(formatter)
    logger = logging.getLogger('pythonConfig')
    logger.setLevel(LOG_LEVEL)
    logger.addHandler(stream)
    if args.logs:
        fh = logging.FileHandler('out/logs.txt','w+')
        fh.setLevel(logging.DEBUG)
        logger.addHandler(fh)
    logger.info(utils.getLogo())

    ###BEGINNING OF THE ACTUAL PROBLEM
    liquidLoader=DataLoader(config.liquiddatafile)
    solidLoader=DataLoader(config.soliddatafile)
    inputData={}
    inputData['liquid']=liquidLoader.load()
    inputData['solid']=solidLoader.load()
    rocketModels=config.rockets.copy()
    graphed=[]
    for rocketName,rocketData in rocketModels.items():
        for blockIndex in range(len(rocketData)):
            analysisName=rocketName + " | " + rocketData[blockIndex]['name']
            logger.info(''.join(["#"]*(len(analysisName)+15)))
            logger.info("Solving rocket "+analysisName)
            engineType=rocketData[blockIndex]['type']
            engineName,engineData=utils.getEngineData(inputData[engineType], rocketData[blockIndex]['index'])
            rocketModels[rocketName][blockIndex]['engName']=engineName
            unsolvedModel=utils.getUnsolvedModel(engineType)
            #INJECT SPECIFIC STAGE DATA
            unsolvedModel['t_b']=InputVariable("Tempo di combustione",'s',rocketData[blockIndex]['tEnd']-rocketData[blockIndex]['tStart'])
            unsolvedModel['z']=InputVariable("Quota",'m',np.linspace(rocketData[blockIndex]['zStart'],rocketData[blockIndex]['zEnd'],100))
            ###
            modelData=utils.mergeData([engineData,unsolvedModel])
            if args.all:
                task=[key for key,val in modelData.items() if isinstance(val,UnknownVariable)]
            else:
                task=[key for key in utils.getOutputs() if key in modelData]

            #LET'S SOLVE
            if engineType not in graphed or True:
                graph=args.graph
                graphed.append(engineType)
            else:
                graph=False

            grph=Grapher(analysisName,graph=graph,view=(not args.noshow),debug=args.debug,cool=args.cool,labels=args.labels)

            slvr=Solver(modelData,task,grph,logger)
            utils.tic()
            try:
                if slvr.validateTree():
                    logger.debug("Tree building took %s seconds"%(utils.toc()))
                    logger.debug("Solving tree...")
                    utils.tic()
                    res=slvr.solve()
                    logger.debug("Done! Solving took %s seconds."%(utils.toc()))
                    logger.info("Here are your outputs:\n"+utils.formatData(slvr.data,engineData,task,engineType))
                    logger.debug("\n"+pp.pformat({key:val.getValue() for key,val in slvr.data.items()}))
                    rocketModels[rocketName][blockIndex]['solvedData']=copy.deepcopy(slvr.data)
                    unusedVariables=slvr.findUnusedVariables()
                    if len(unusedVariables):
                        logger.warning("There are some unused input varables: %s\n"%(str(unusedVariables)))
                    if args.graph:
                        grph.export()
            except Exception:
                 print(traceback.format_exc())

    if args.nozzleplot:
        nozzleplotter=NozzlePlotter(rocketModels)
        nozzleplotter.make()

    if args.compare:
        comparer=Comparer(rocketModels)
        comparer.make()

    if args.postproc:
        postProcesser=PostProcesser(rocketModels)
        postProcesser.make()

    if args.latex:
        latexer=Latexer(rocketModels)
        latexer.make()

    if args.outputcea:
        outputcea=OutputCea(rocketModels)
        outputcea.make()

    #pp.pprint(rocketModels)
    if not args.noshow:
        plt.ioff()
        plt.show()
