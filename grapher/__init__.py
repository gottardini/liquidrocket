import matplotlib.pyplot as plt
import networkx as nx

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

class Grapher:
    def __init__(self):
        self.G=nx.DiGraph()
        self.initialized=False

    def addNode(self,name,description,parent=None):
        self.G.add_node(name,description=description)
        if parent is not None:
            self.G.add_edge(name,parent)
        self.drawGraph()

    def pause(self,val):
        plt.pause(val)

    def drawGraph(self):
        if not self.initialized:
            self.fig, self.ax = plt.subplots(figsize=(8, 8))
            #self.ax.('equal')
            self.initialized=True
        #self.pos = nx.planar_layout(self.G)
        self.pos = nx.circular_layout(self.G)
        #self.pos = graphviz_layout(self.G, prog='twopi', args='')
        #print(self.pos)
        self.ax.cla()
        nx.draw_networkx(self.G, self.pos, ax=self.ax, node_size=50, alpha=0.5, with_labels=False, node_color="blue",linewidths=1,arrowsize=20)
        pos_attrs = {}
        for node, coords in self.pos.items():
            pos_attrs[node] = (coords[0], coords[1] + 0.1)
        node_attrs = nx.get_node_attributes(self.G, 'description')
        nx.draw_networkx_labels(self.G, pos_attrs, ax=self.ax, labels=node_attrs)

        self.fig.canvas.draw()
        #plt.show(block=True)
