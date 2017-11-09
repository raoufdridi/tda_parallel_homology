import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

class simplicialcomplex(object):
    def __init__(self, simplices):
        res = []
        for l in simplices:
            res +=l
        self.simplices = res
        if len(simplices)>0: 
            self.vertices = simplices[0]
        else:
            self.vertices = []
        if len(simplices)>1: 
            self.edges = simplices[1]
        else:
            self.edges = []
        if len(simplices)>2: 
            self.triangles = simplices[2]
        else:
            self.triangles = []
        if len(simplices)>3:
            self.tetrahedra = simplices[3]
        else:
            self.tetrahedra = []
    def graph(self):
        G = nx.Graph(self.edges)
        return G
    def get_cover(self, solver='sage'):
    	G = self.graph()
    	return 0

   

def intersecting_pairs_at_vertices(partition):
    # list all pairs of vertex-intersecting subcomplexes
    res =[]
    for i in range(0, len(partition)):
        K1 = partition[i]
        for j in range(i+1, len(partition)):
            K2 = partition[j]
            if len(set(K1.vertices).intersection(set(K2.vertices)))!=0:
                res += [(K1, K2)]
    return res


def intersecting_pairs_at_edges(partition):
    res =[]
    #print partition
    for i in range(0, len(partition)):
        K1 = partition[i]
        for j in range(i+1, len(partition)):
            K2 = partition[j]
            #print i, j
            if len(my_intersection(K1.edges, K2.edges)) !=0:
                res += [(K1, K2)]
    return res

def intersecting_triplets_at_vertices(partition):
    res =[]
    for i in range(0, len(partition)):
        K1 = partition[i]
        for j in range(i+1, len(partition)):
            K2 = partition[j]
            for k in range(j+1, len(partition)):
                K3 = partition[k]
                if len(set(K1.vertices).intersection(set(K2.vertices)).intersection(set(K3.vertices)))!=0:
                    res += [(i, j, k)]
                    #print i, j, k, (set(K1.vertices).intersection(set(K2.vertices)).intersection(set(K3.vertices)))
    return res



def my_intersection(l1, l2): #preserves the initial ordering
    res = []
    for x in l1:
        if x in l2:
            res+=[x]
    return res

          





def main():
        K = simplicialcomplex([["a", "b", "c", "d"], [("a", "b"), ("b", "c"), ("c", "d")]])
        K0 = simplicialcomplex([["a", "b", "c"], [("a", "b"), ("b", "c")]])
        K1 = simplicialcomplex([["b", "c", "d"], [("b", "c"), ("c", "d")]])

        # print "K0.simplices----->", K0.simplices 
        # print "K1.simplices----->", K1.simplices 

        # print "edge_derivative2((K0, K1), [K0, K1], 1)----->", edge_derivative2((K0, K1), [K0, K1], 1)    
        # print "edge_derivative2((K0, K1), [K0, K1], 0)----->", edge_derivative2((K0, K1), [K0, K1], 0)
        # print "d0([K0, K1],  0)---->", d0([K0, K1],  0)
        # print "d0([K0, K1],  1)---->", d0([K0, K1],  1)

        H = simplicialcomplex([["a", "b", "c", "d", "e", "f"], [("a", "b"), ("b", "c"), ("c", "d"), ("d", "e"), ("e", "f")]])
        H0= simplicialcomplex([["a", "b", "c"], [("a", "b"), ("b", "c")]])
        H1= simplicialcomplex([["b", "c", "d", "e"], [("b", "c"), ("c", "d"), ("d", "e")]])
        H2= simplicialcomplex([["d", "e", "f"], [("d", "e"), ("e", "f")]])

        partition = [H0, H1, H2]
        d0(partition, 0)
        d0(partition, 1)
        d0(partition, 2)


        O1 = simplicialcomplex([["a", "b", "c", "d"],
                              [("a", "b"), ("b", "c"), ("a", "c"), ("c", "d")], [("a", "b", "c")]])
        O2 = simplicialcomplex([["a", "b", "c", "e"],
                              [("a", "b"), ("b", "c"), ("a", "c"), ("b", "e")], [("a", "b", "c")]])

        # print "O1 --->", O1.simplices
        # print "O2 --->", O2.simplices
        # print "d1([O1, O2], 0)----->", d1([O1, O2], 0)
        # print "d1([O1, O2], 1)----->", d1([O1, O2], 1)
        # print "d1([O1, O2], [0, 1])----->", d1([O1, O2], [0, 1])

    	K = simplicialcomplex([["0", "1", "2", "3", "4", "5", "6"],
    	                      [("0", "1"), ("1", "2"), ("2", "3"), ("0", "3"),
    	                       ("3", "4"), ("0", "4"), ("4", "5"), ("5", "6"), ("2", "6")], [("0", "3", "4")]])


    	K0 =simplicialcomplex([["0", "3", "4"], [("0", "3"), ("3", "4"), ("0", "4")], [("0", "3", "4")]])
    	K1 = simplicialcomplex([["1", "2"], [("1", "2")]])
    	K2 = simplicialcomplex([["5", "6"], [("5", "6")]])
    	K3 = simplicialcomplex([["0", "1", "2", "3", "4", "5", "6"], 
    		[("0", "1"),  ("2", "3"), ("2", "6"),("4", "5")]])


    	partition = [K0, K1, K2, K3]

    	print K.get_cover()
    	#print edge_derivative1(K0)

if __name__ == '__main__':
    main()

