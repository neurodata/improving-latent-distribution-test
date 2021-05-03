import networkx as nx
from graspologic.utils import remove_loops, symmetrize, binarize


def convert_classes(to_change):
    simple_classes = ['PN', 'APL', 'MBIN', 'MBON', 'KC']
    
    out = []
    for string in to_change:
        for simple_class in simple_classes:
            if simple_class in string:
                out.append(simple_class)
                
    return out


def load_data(symmetric=True, binary=True):
    G = nx.read_graphml("./data/G.graphml")

    G_l = G.subgraph([node for node, data in G.nodes(data=True) if data['Hemisphere'] == 'left'])
    A_l = remove_loops(nx.to_numpy_array(G_l))
    nodes_l = convert_classes([data['Class'] for node, data in G_l.nodes(data=True)])

    G_r = G.subgraph([node for node, data in G.nodes(data=True) if data['Hemisphere'] in ['right', 'center']])
    A_r = remove_loops(nx.to_numpy_array(G_r))
    nodes_r = convert_classes([data['Class'] for node, data in G_r.nodes(data=True)])

    hemispheres = ['Left'] * 163 + ['Right'] * 158
    
    if symmetric:
        A_l = symmetrize(A_l, 'avg')
        A_r = symmetrize(A_r, 'avg')
        
    if binary:
        A_l = binarize(A_l)
        A_r = binarize(A_r)

    return A_l, nodes_l, A_r, nodes_r, hemispheres