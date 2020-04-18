import utils
print(utils.getLogo())
from solver import Solver
from grapher import Grapher
from postprocessing import PostProcesser
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
    parser.set_defaults(graph=False)
    parser.set_defaults(debug=False)
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


    outputs=utils.getOutputs()
    data=utils.getData(0)
    grph=Grapher(view=args.graph,debug=args.debug)
    postprocesser=PostProcesser()
    try:
        logger.info("Requested outputs: ")
        logger.info(pp.pformat([(out,data[out].description) for out in outputs]))
        print()
        logger.info("Building problem tree...")
        slvr=Solver(data,outputs,grph,logger)
        #time.sleep(6)
        utils.tic()
        if slvr.validateTree():
            logger.info("Tree building took %s seconds"%(utils.toc()))
            logger.info("Solving tree...")
            utils.tic()
            res=slvr.solve()
            logger.info("Done! Solving took %s seconds. Here are your results:"%(utils.toc()))
            logger.info(res)
            logger.debug("\n"+pp.pformat({key:val.getValue() for key,val in slvr.data.items()}))
            logger.info("Postprocessing...")
            postprocesser.make(slvr.data)
    except Exception:
         print(traceback.format_exc())
    plt.show()
