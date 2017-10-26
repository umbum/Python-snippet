#-*-coding:utf-8-*-
from collections import OrderedDict
from pprint import pprint

import networkx as nx
from plotly.graph_objs import *
from plotly.offline import plot




def build_graph():
    G = nx.DiGraph()
    
    self.G.add_node(1, status=0)
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
    def __init__(self):
        self.G = dict()
        self.traces = dict()
        
    def set_graph(self, G, key):
        self.G[key] = G
        self.traces[key] = self._init_traces()
        self.graph_to_traces(key)
    
    def _init_traces(self):
        #앞에서 부터 그리기 때문에 OrderedDict.
        #edge를 나중에 그리면 노드 위에 선이 올라와 지저분해진다.
        traces = OrderedDict()
        
        self.traces['edge'] = Scatter(
            name = 'links'
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
                size = [],
                opacity=1,
                colorscale='YlGnBu',
                color=[],
                line = {'width':1, 'color':'#555'}
                )
            )
            
            
        return traces
    
    def get_pos(self):
        return nx.circular_layout(self.G)
    '''
    nx.nx_agraph.graphviz_layout(self.G, prog="twopi", root=0) : pygraphviz
    nx.nx_pydot.graphviz_layout(self.G, prog="twopi", root=0)  : pydot 
    nx의 graphviz_layout 메소드를 호출하면 자동으로 pygraphviz/pydot가 import되며 실행된다.
    근데 이거 꽤나 느리다. 호출하면 graphviz\\bin\\twopi.exe가 실행되며 pos값을 temp 파일에 쓰고, 
    python에서 temp 파일을 읽어와 반환하는 방식이다.
    파일을 읽어와 반환하는 작업까지 한꺼번에 연결되어 있어 그냥은 최적화가 어렵다.
    '''
    
    def graph_to_traces(self.key):
        G = self.G[key]
        traces = self.traces[key]
        pos = self.get_pos(key)
        
        #init root
        root_x = pos[0][0]
        root_y = pos[0][1]

        for node, data in G.node.items():
            x, y = pos[node]
            if G.node[node]['status'] == 0:
                pass
            else:
                trace = 'node'
            self.traces[trace]['x'].append(x)
            self.traces[trace]['y'].append(y)
            text = ''
            for key, value in data.items():
                text += key + " : " + str(value) + "<br />"
            self.traces[trace]['text'].append(text)
            self.traces[trace]['marker']['color'].append(((x - root_x)**2 + (y - root_y)**2)**0.5)
            # colorscale이 지정되어 있는 경우, 
            # color에 대충 값만 지정해도 알아서 값에 비례한 색상으로 바꿔준다.
            self.traces[trace]['marker']['size'].append(9 + len(G.edge[node]))

        
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            self.traces['edge']['x'] += [x0, x1, None]
            self.traces['edge']['y'] += [y0, y1, None]
            
    
    def table(self, fname):
        tbl = [[]]
        
        ''' 처음부터 모든 리스트를 결합해 set으로 추려 n*m np.array를 할당하는
        방식으로 진행하면 여기에 데이터를 채울 때 또 다시 반복을 돌아야 해서
        2번 반복해야 한다.
        이렇게 리스트를 붙여나가는 식으로 하면 한 번만 반복해도 됨.'''
        for key in self.traces.keys():
            tbl.append(['-' for x in range(len(tbl[0]))])
            for node in self.G[key].node.values():
                try:
                    idx = tbl[0].index[node['filename']]
                    tbl[-1][idx] = node['status']
                except ValueError:
                    tbl[0].append(node['filename'])
                    tbl[-1].append(node['status'])
                    
        # transpose
        tbl_t = list(zip(*tbl))
        
        # sort
        tbl_t_s = sorted(tbl_t, key=lambda x : x[0])
        
        tbl_t_s.insert(0, ["node", *[col for col in self.traces.keys()]])
        figure = ff.create_table(tbl_t_s)
        plot(figure, filename=fname)
        
        
    def visualize(self, key, fname):
        plot(Figure(data=Data(self.traces[key].values()),
        layout=Layout(
            hovermode='closest',
            xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False)
            )
        ), filename = fname)
        
        
        
if __name__ == "__main__":
    v = Visualization()
    
    G = build_graph()
    v.set_graph(G, 'graph1')
    
    v.visualize('graph1', 'graph1.html')
    v.table('table.html')
    
