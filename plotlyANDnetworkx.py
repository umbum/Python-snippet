
from plotly.graph_objs import *
from plotly.offline import plotly

import networkx as networkx

class GraphPos:
    def __init__(self):
        self.G = nx.DiGraph()
        self.build_graph()
        self.pos = self.set_pos()

    def build_graph(self):
        self.G.add_node(1)
        self.G.add_nodes_from(range(2, 50))
        self.G.add_edges_from([(1, x) for x in range(2, 50)])

    def set_pos(self):
        return nx.circular_layout(self.G)
# nx.nx_agraph.graphviz_layout(self.G, prog="towpi", args='') : pygraphviz
# nx.nx_pydot.graphviz_layout(self.G, prog="towpi", args='')  : pydot 
# 함수를 호출하면 자동으로 import된다.
		
		
		
GPos = GraphPos()

#plotly
node_trace = Scatter(
    x = [],
    y = []
)
edge_trace = Scatter(
    x = [],
    y = []
)

for node in GPos.G.nodes():
    x, y = GPos.pos[node]
    node_trace['x'].append(x)
    node_trace['y'].append(y)

for edge in GPos.G.edges():
    x0, y0 = GPos.pos[edge[0]]
    x1, y1 = GPos.pos[edge[1]]
    edge_trace['x'] += [x0, x1, None]
    edge_trace['y'] += [y0, y1, None]
