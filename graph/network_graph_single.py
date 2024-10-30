from collections import OrderedDict
from pprint import pprint

import networkx as nx
from plotly.graph_objs import Scatter, Figure, Layout
from plotly.offline import plot


def buildTestGraph():
    G = nx.DiGraph()

    G.add_node(1, status=0)
    G.add_nodes_from(range(2, 32))
    G.add_edges_from([(1, x) for x in range(2, 30)])
    #15-20은 1에도 연결되어 있기 때문에 1과의 동심원이 우선한다.
    G.add_edges_from([(5, x) for x in range(15, 20)])

    #얘네는 1과 연결되어 있지 않기 때문에 바깥 동심원에 위치.
    G.add_edge(29, 30)
    G.add_edge(29, 31)

    #더 바깥 동심원.
    G.add_edge(30, 32)

    return G


class GraphVisualizer:
    def __init__(self, G):
        self.G = G
        self.node_trace, self.edge_trace = self.initTrace()
        self.assignTraceUsingGraph()

        self.node_trace = Scatter(self.node_trace)
        self.edge_trace = Scatter(self.edge_trace)

    def initTrace(self):
        node_trace = dict(
            name = 'host',
            x = [],
            y = [],
            hoverinfo = 'text',
            text = [],
            mode = 'markers',
            marker = dict(
                size = [],
                opacity=1,
                colorscale='YlGnBu',
                color=[],
                line = {"width":2, 'color':'#555'}
            )
        )

        edge_trace = dict(
            name = 'link',
            x = [],
            y = [],
            hoverinfo='none',
            mode = 'lines',
            line = dict(width=0.5, color='#888')
        )
        return node_trace, edge_trace

    def getLayoutPos(self, G):
        return nx.drawing.random_layout(G)
        '''
        nx.nx_agraph.graphviz_layout(self.G, prog="twopi", root=0) : pygraphviz
        nx.nx_pydot.graphviz_layout(self.G, prog="twopi", root=0)  : pydot 
        nx의 graphviz_layout 메소드를 호출하면 자동으로 pygraphviz/pydot가 import되며 실행된다.
        근데 이거 꽤나 느리다. 호출하면 graphviz\\bin\\twopi.exe가 실행되며 pos값을 temp 파일에 쓰고, 
        python에서 temp 파일을 읽어와 반환하는 방식이다.
        파일을 읽어와 반환하는 작업까지 한꺼번에 연결되어 있어 그냥은 최적화가 어렵다.
        '''


    def assignTraceUsingGraph(self):
        G = self.G
        pos = self.getLayoutPos(G)

        #init root
        root_x = pos[1][0]
        root_y = pos[1][1]

        for id, data in G.node.items():
            x, y = pos[id]
            self.node_trace['x'].append(x)
            self.node_trace['y'].append(y)

            text = ''
            for key, value in data.items():
                text += "{} : {}<br />".format(key, str(value))
            self.node_trace['text'].append(text)
            self.node_trace['marker']['color'].append(((x - root_x) ** 2 + (y - root_y) ** 2) ** 0.5)
            self.node_trace['marker']['size'].append(20)
            # colorscale이 지정되어 있는 경우, color에 대충 값만 지정해도 알아서 값에 비례한 색상으로 바꿔준다.

        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            self.edge_trace['x'].append([x0, x1, None])
            self.edge_trace['y'].append([y0, y1, None])


    def table(self, fname):
        tbl = [[]]
        ''' 처음부터 모든 리스트를 결합해 set으로 추려 n*m np.array를 할당하는
        방식으로 진행하면 여기에 데이터를 채울 때 또 다시 반복을 돌아야 해서
        2번 반복해야 한다.
        이렇게 리스트를 붙여나가는 식으로 하면 한 번만 반복해도 됨.'''
        for key in self.trace.keys():
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

        tbl_t_s.insert(0, ["node", *[col for col in self.trace.keys()]])
        figure = ff.create_table(tbl_t_s)
        plot(figure, filename=fname)


    def visualize(self, fname):
        print(self.node_trace)
        plot(Figure(data=[self.edge_trace, self.node_trace],
                    layout=Layout(
                        hovermode='closest',
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                    )
                    ), filename = fname)



if __name__ == "__main__":
    G = buildTestGraph()
    v = GraphVisualizer(G)

    v.visualize('graph1.html')
    # v.table('table.html')
