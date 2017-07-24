#-*-coding:utf-8-*-
from plotly.graph_objs import *
from plotly.offline import plot
from collections import OrderedDict

import networkx as nx



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
    def __init__(self, G):
        self.G = G
        #앞에서 부터 그리기 때문에 OrderedDict.
        #edge를 나중에 그리면 노드 위에 선이 올라와 지저분해진다.
        self.traces = OrderedDict()
        self.graph_to_traces()
    
    def get_pos(self):
        return nx.circular_layout(self.G)
    '''
    nx.nx_agraph.graphviz_layout(self.G, prog="twopi", root=1) : pygraphviz
    nx.nx_pydot.graphviz_layout(self.G, prog="twopi", root=1)  : pydot 
    nx의 graphviz_layout 메소드를 호출하면 자동으로 pygraphviz/pydot가 import되며 실행된다.
    근데 이거 꽤나 느리다. 호출하면 graphviz\\bin\\twopi.exe가 실행되며 pos값을 temp 파일에 쓰고, 
    python에서 temp 파일을 읽어와 반환하는 방식이다.
    파일을 읽어와 반환하는 작업까지 한꺼번에 연결되어 있어 그냥은 최적화가 안된다.
    데커레이터를 사용하면 가능할 것 같은데 안해봤다.
    '''
    
    def set_colorscale(self):
        # colorscale이 지정되어 있는 경우, 
        # color에 대충 값만 지정해도 알아서 값에 비례한 색상으로 바꿔준다.
        
        root_x = self.traces['root']['x'][0]
        root_y = self.traces['root']['y'][0]
        for idx in range(len(self.traces['node']['x'])):
            x = self.traces['node']['x'][idx]
            y = self.traces['node']['y'][idx]
            self.traces['node']['marker']['color'].append(((x - root_x)**2 + (y - root_y)**2)**0.5)
            
    def hover_effect(self):
        for node in range(len(self.traces['node']['x'])):
            self.traces['node']['text'].append(str(node))
            
    def graph_to_traces(self):
        G = self.G
        pos = self.get_pos()

        self.traces['edge'] = Scatter(
            x = [],
            y = [],
            hoverinfo='none',
            mode = 'lines',
            line = Line(width=0.5, color='#888')
            )
            
        self.traces['node'] = Scatter(
            name = 'nodes',
            x = [],
            y = [],
            hoverinfo = 'text',
            text = [],
            mode = 'markers',
            marker = Marker(
                size = 9,
                colorscale='YlGnBu',
                color=[],
                line = dict(width=1.3)
                )
            )
            
        self.traces['root'] = Scatter(
            name = 'root',
            x = [pos[0][0]],
            y = [pos[0][1]],
            hoverinfo = 'text',
            text = ['root'],
            mode = 'markers',
            marker = Marker(
                size = 12,
                color='#ff2a25',
                line = dict(width=1)
                )
            )        

        for node in G.nodes():
            x, y = pos[node]
            self.traces['node']['x'].append(x)
            self.traces['node']['y'].append(y)
        
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            self.traces['edge']['x'] += [x0, x1, None]
            self.traces['edge']['y'] += [y0, y1, None]
            

        # delete root from node trace
        del self.traces['node']['x'][0]
        del self.traces['node']['y'][0]
        
        self.hover_effect()
        self.set_colorscale()
        
        
        
    def visualize(self):
        plot(Figure(data=Data(self.traces.values()),
        layout=Layout(
            hovermode='closest',
            xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False)
            )
        ), filename = "static")
        
        
        
if __name__ == "__main__":
    G = build_graph()
    v = Visualization(G)
    v.visualize()
