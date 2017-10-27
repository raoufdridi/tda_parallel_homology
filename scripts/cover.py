
import networkx as nx
from simplicial_complex import *
from parallel_rank import *


def get_clique_cover(dwave_res):
    # take a dwave_coloring which is a dict and returns the actual vertex clique cover
    return dwave_res[0].values()

def mapping(clique):
    res = dict({})
    for i in range(0, len(clique)):
        res[i]= clique[i]
    return res

def extend_graph_cover_to_simplicial_complex_cover(cliques, K):
    # clique is such the example:
    # dwave_res = dwave_coloring(G, 3)
    # cliques = get_cliques_cover(dwave_res, G, 3)
    simp_cover =[]
    graph_cover =dict({})
    for i in range(0, len(cliques.values())):
        clique = cliques.values()[i]
        new_labels = mapping(clique)
        simp_cover += [ complete_cover(nx.relabel_nodes(nx.complete_graph(len(clique)), new_labels), K)]
    
    #print map(lambda x: x.simplices, simp_cover)
    return simp_cover + [last_covering_set_complete(simp_cover, K)]

def complete_cover(G, simpc): # G is a susbgraph of simpc.graph()
    
    if set(G.nodes()).intersection(set(simpc.vertices))=={}:
        return "given graph is not a susbgraph of simpc.graph()"
    for edge in G.edges():
        if not edge in simpc.edges: 
            return "given graph is not a susbgraph of simpc.graph()"
    
    Kedges =[]
    Ktriangles =[]
    Ktetrahedra =[]
    for e in simpc.simplices:
        if len(e) ==2 and set(e).issubset(G.nodes()):
            Kedges +=[e]
        elif len(e) ==3 and set(e).issubset(G.nodes()):
            Ktriangles +=[e]
        elif len(e) ==4 and set(e).issubset(G.nodes()):
            Ktetrahedra +=[e]
    return simplicialcomplex([G.nodes(), Kedges, Ktriangles, Ktetrahedra])


def last_covering_set_complete(partition_except_last, K):
    res = simplicialcomplex([[], [], [], []])
    resvertices = []
    resedges = []
    restriangles =[]
    restetrahedra =[]
    bag =[]
    
    for Ki in partition_except_last:
        bag += Ki.simplices
        #bag += Ki.edges
        #bag += Ki.triangles
        #bag += Ki.tetrahedra
    for simplex in K.simplices:
        if not simplex in bag:
            if len(simplex)==2:
                resedges += [simplex]
            elif len(simplex) ==3:
                restriangles += [simplex]
            elif len(simplex) ==4:
                restetrahedra
    extra_bag =[]            
    for simplex in resedges + restriangles + restetrahedra:
        #print simplex
        extra_bag += simplex 
        #print extra_bag
    for v in K.vertices:
        #print v
        if v in extra_bag:
            #print "hi"
            resvertices += [v]
    res = simplicialcomplex([resvertices, resedges, restriangles, restetrahedra]) 
    return res
        

def coloring(G, partition):
    def my_function(v):
        for i in range(0, len(partition)-1):
            if v in partition[i].vertices:
                return i
    return [my_function(v) for v in G.nodes()]