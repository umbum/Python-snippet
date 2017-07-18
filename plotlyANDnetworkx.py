
from plotly.graph_objs import *
from plotly.offline import plotly

import networkx as networkx


def build_graph():
    G = nx.DiGraph()
    
    self.G.add_node(1)
    self.G.add_nodes_from(range(2, 32))
    self.G.add_edges_from([(1, x) for x in range(2, 30)])
    #15-20은 1에도 연결되어 있기 때문에 1과의 동심원이 우선한다.
    self.G.add_edges_from([(5, x) for x in range(15, 20)])
    
    #얘네는 1과 연결되어 있지 않기 때문에 바깥 동심원에 위치.
    self.G.add_edge(29, 30)
    self.G.add_edge(29, 31)
    
    #더 바깥 동심원.
    self.G.add_edge(30, 32)
    
    return G
		

#plotly		
class Visualization:
    def get_pos(self, G):
        return nx.circular_layout(G)
    # nx.nx_agraph.graphviz_layout(G, prog="towpi", root=1) : pygraphviz
    # nx.nx_pydot.graphviz_layout(G, prog="towpi", root=1)  : pydot 
    # 함수를 호출하면 자동으로 import된다.
    
    def make_data(self):
        G = build_graph()
        pos = self.get_pos(G)
                
        node_trace = Scatter(
            x = [],
            y = [],
            hoverinfo = 'text',
            text = [],
            mode = 'markers',
            marker = Marker(
                size = 10
                ),
            line = dict(width=2)
        )
        
        edge_trace = Scatter(
            x = [],
            y = [],
            hoverinfo='none',
            mode = 'lines',
            line = Line(width=0.5, color='#888')
        )

        for node in G.nodes():
            x, y = pos[node]
            node_trace['x'].append(x)
            node_trace['y'].append(y)
        
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_trace['x'] += [x0, x1, None]
            edge_trace['y'] += [y0, y1, None]
        
        self.hover_effect(G, node_trace)
        
        return Data([node_trace, edge_trace])
        
    def hover_effect(self, G, node_trace):
        for node in G.nodes():
            node_trace['text'].append(str(node))
        
    def visualize(self):
        plot(Figure(data=self.make_data(),
        layout=Layout(
            hovermode='closest',
            xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False)
            )
        ), filename = "static")
        
if __name__ == "__main__":
    v = Visualization()
    v.visualize()
