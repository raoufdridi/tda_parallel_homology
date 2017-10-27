import networkx as nx
from simplicial_complex import *


def completegraph(lst):
    res = nx.Graph()
    res.add_nodes_from(lst)
    for i in xrange(len(lst)):
        for j in range(i+1, len(lst)):
            res.add_edge(lst[i], lst[j])
    return res
    
def powerset(lst):
    return reduce(lambda result, x: result + [subset + [x] for subset in result],
                  lst, [[]])


def cleaning(sigma, K): # reorder sigma wrt to the ordering of K. eg., [1, 0] is ordered as [0, 1]
    simplices = K.simplices
    for simplex in simplices:
        if type(simplex) ==tuple:
            if set(sigma)== set(simplex):
                return simplex
    
    
def all_cliques(G):
    # internal: used in clique_complex              
    #not counting the vertices
    maximal_cliques = list(nx.find_cliques(G))
    #print (maximal_cliques)
    N = max(map(len, maximal_cliques))
    res = dict({})
    for i in range(2, N+1):
        res[i]=[]
    for clique in maximal_cliques:
        subcliques = powerset(clique)[1:-1]
        for subclique in subcliques:
            if len(subclique)!=1:
                #print subclique
                #print res.values()
                if not subclique in res[len(subclique)]:
                    res[len(subclique)] +=[subclique]
    fres =[]
    for key in res.keys():
        fres += res[key] 
    return   fres + maximal_cliques


def clique_complex(G):
    res = dict({})
    cliques = all_cliques(G)
    N = max(map(len, cliques))
    res = dict({})
    for i in range(2, N+1):
        res[i]=[]    
    for clique in cliques:
        res[len(clique)] += [tuple(clique)] # tuples are used in simplicialcomplex def
        
    return simplicialcomplex([G.nodes()] + [res[l] for l in range(2, N+1)])
    
def clique_subcomplex(G, K):
    res = dict({})
    #print G.nodes()
    if len(G.nodes())==1:
        return simplicialcomplex([G.nodes()]) 
    cliques = [cleaning(tuple(clique), K) for clique in all_cliques(G)] # make sure all clique are ordered properly
    #print all_cliques(G)
    #print K.simplices
    N = max(map(len, cliques))
    #print N
    res = dict({})
    for i in range(2, N+1):
        res[i]=[]    
    for clique in cliques:
        res[len(clique)] += [clique]
        
    return simplicialcomplex([G.nodes()] + [res[l] for l in range(2, N+1)])


def extra_bag(K, Ki_list):
    simplices = []
    Ksimplices = K.simplices
    N = len(Ksimplices[-1])
    res = dict({})
    for i in range(2, N+1):
        res[i]=[]
    vertices = set()
    for simplex in Ksimplices:
        if type(simplex)==tuple:
            Flag = True
            for Ki in Ki_list:
                Flag = not (set(simplex).issubset(set(Ki.vertices))) and Flag
            if Flag:
                    #print "set(simplex)", simplex
                    #print "set(Ki.vertices)", set(Ki.vertices)
                    #print "(set(simplex).issubset(set(Ki.vertices)))", (set(simplex).issubset(set(Ki.vertices)))
                    
                    res[len(simplex)] += [simplex] 
                    vertices = vertices.union(set(simplex)) # get the vertices in the same time,
                                                            # not always equal to K.vertices
    #print list(vertices)
    fvertices = []
    for v in K.vertices:
        if v in vertices: fvertices +=[v]  # to ge the same ordering as K.vertices
            
    fres = [list(fvertices)] + [res[l] for l in range(2, N+1)]
    if [] in fres:fres.remove([])
    #print fres
    return simplicialcomplex(fres)
    
         