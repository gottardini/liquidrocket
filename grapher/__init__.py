import matplotlib.pyplot as plt
import networkx as nx
from collections import OrderedDict
from matplotlib.collections import LineCollection
from fa2 import ForceAtlas2
from grapher.curved_edges import curved_edges
import copy

#plt.ion()

try:
    import pygraphviz
    from networkx.drawing.nx_agraph import graphviz_layout
except ImportError:
    try:
        import pydot
        from networkx.drawing.nx_pydot import graphviz_layout
    except ImportError:
        raise ImportError("Need Graphviz and either "
                          "PyGraphviz or pydot")

forceatlas2 = ForceAtlas2()

class Grapher:
    def __init__(self,name,graph=True,view=False,debug=False,cool=False,labels=False):
        self.name=name
        self.G=nx.DiGraph()
        self.initialized=False
        self.colors=OrderedDict()
        self.view=view
        self.debug=debug
        self.cool=cool
        self.labels=labels
        self.graph=graph

    def addNode(self,name,description,parent=None):
        self.G.add_node(name,description=description)
        if name not in self.colors:
            self.colors[name]='#000000'
        if parent is not None:
            self.G.add_edge(name,parent)
        if self.graph and self.debug:
            self.drawGraph()

    def pause(self,val):
        plt.pause(val)

    def changeNodeColor(self,node,color):
        self.colors[node]=color
        if self.graph and self.debug:
            self.drawGraph()

    def calcPos(self):
        if self.cool:
            self.pos= forceatlas2.forceatlas2_networkx_layout(self.G, pos=None, iterations=50)
        else:
            #self.pos = nx.planar_layout(self.G)
            #self.pos = nx.shell_layout(self.G)
            #self.pos = nx.spiral_layout(self.G)
            #self.pos = nx.kamada_kawai_layout(self.G)
            #self.pos = nx.spectral_layout(self.G)
            #self.pos = nx.circular_layout(self.G)
            #self.pos = nx.random_layout(self.G)
            self.pos = graphviz_layout(self.G, prog='twopi', args='')

    def export(self):
        if self.graph:
            self.fig.savefig("out/graph/pb_graph_%s.svg"%self.name)

    def drawGraph(self):
        if not self.graph:
            return
        #print(self.G.number_of_nodes())
        if not self.initialized:
            self.fig=plt.figure(figsize=(8, 8),num=self.name)
            self.ax=self.fig.add_axes([0,0,1,1])
            #self.fig, self.ax = plt.subplots(figsize=(8, 8),num='Liquid rocket analysis',facecolor='white')
            if self.view:
                plt.ion()
                plt.show()
            #self.fig.tight_layout()
            self.ax.set_axis_off()
            self.initialized=True
        self.ax.cla()
        self.ax.set_axis_off()
        self.calcPos()
        if self.cool:
            curves = curved_edges(self.G, self.pos)
            lc = LineCollection(curves, color='k', alpha=0.2)
            nx.draw_networkx_nodes(self.G, self.pos, node_size=50, node_color='k', alpha=0.9)
            self.ax.add_collection(lc)
            plt.tick_params(axis='both',which='both',bottom=False,left=False,labelbottom=False,labelleft=False)
        else:
            #tcolors=[node[1] for node in list(self.colors.items())]
            #print(tcolors)
            #nx.draw_networkx(self.G, self.pos, ax=self.ax, node_size=50, alpha=1, with_labels=False, node_color=tcolors,linewidths=1)
            #nx.draw_networkx(self.G, self.pos, ax=self.ax, node_size=50, alpha=1, with_labels=False, node_color='#222222',linewidths=1, edge_color=(0.5,0.5,0.5,0.01))
            nx.draw_networkx_nodes(self.G, self.pos, ax=self.ax, node_size=30, node_color='#222222')
            nx.draw_networkx_edges(self.G, self.pos, ax=self.ax, node_size=40, linewidths=2, edge_color='#000000', alpha=0.2)
            if self.labels:
                pos_attrs = {}
                for node, coords in self.pos.items():
                    pos_attrs[node] = (coords[0] + 0.02, coords[1] + 5)
                node_attrs = nx.get_node_attributes(self.G, 'description')
                nx.draw_networkx_labels(self.G, pos_attrs, ax=self.ax, labels=node_attrs)

        self.pause(0.01)
