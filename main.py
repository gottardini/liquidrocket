import config
from solver import Solver
from grapher import Grapher
import time
import matplotlib.pyplot as plt
import traceback
import argparse
import pprint
pp=pprint.PrettyPrinter()


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

    outputs=config.getOutputs()
    data=config.getData(0)
    grph=Grapher(view=args.graph,debug=args.debug)
    try:
        print("Requested outputs: ")
        pp.pprint([(out,data[out].description) for out in outputs])
        print("\nBuilding problem graph...")
        slvr=Solver(data,outputs,grph)
        if slvr.validateTree():
            print("Solving...")
            res=slvr.solve()
            print("Done! Here are your results:")
            pp.pprint(res)
    except Exception:
         print(traceback.format_exc())
    plt.show()
