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

# def edge_derivative2(pair, partition, j):
#     # pair here is a pair of intersecting simp complexes at vertex level
#     # this function computes partial_1 for all edges of the form $v \otimes alpha beta$
#     # with v is a vertex in the intersection 
#     # Returns jth row blow
    
#     res =[] 
#     Kj = partition[j]
#     if Kj in pair:  
#         for v in my_intersection(pair[0].vertices, pair[1].vertices):
#             l = [0 for i in range(0, len(Kj.vertices))]
#             for i in range(0, len(Kj.vertices)):
#                 if v == Kj.vertices[i]:
#                     if pair[0]==Kj:
#                         l[i]=-1
#                     if pair[1]==Kj:
#                         l[i]=1
#             res +=[l]
#     else: # if the intersection with Kj is empty return 0
#         res += [[0 for i in range(0, len(Kj.vertices))] for k in range(0, len(set(pair[0].vertices).intersection(set(pair[1].vertices))))]
#     return res



# def d0(partition, j): # return the jth block of rows
#     Kj = partition[j]
#     A =[]
#     for K in partition:
#         if K==Kj:
#             A+= edge_derivative1(Kj)
#         else:
#             A+= [[0 for i in range(0, len(Kj.vertices))] for k in range(0, len(K.edges))]
            
#     pairs = intersecting_pairs_at_vertices(partition)
#     for pair in pairs:
#         A+= edge_derivative2(pair, partition, j)
    
#     return np.array(A).transpose()

# def triangle_derivative1(K):
#     # eats blowup triangles of the form $abc \otimes i$
#     def triangle_derivative0(T):
#         return [(T[0], T[1]), (T[0], T[2]), (T[1], T[2])]
#     res = []
#     for T in K.triangles:
#         l =[0 for i in range(0, len(K.edges))]
#         triangle_edges = triangle_derivative0(T)
#         #print triangle_edges
#         for i in range(0, len(triangle_edges)):
#             for j in range(0, len(K.edges)):
#                 if triangle_edges[i]== K.edges[j]:
#                        l[j] = (-1)**i
#         res +=[l]
#     return res


# def triangle_derivative2(pair, partition, j):
#     # computes partial_1 of triangles of the for $ab \otimes alpha beta $
#     # ab in common edges for the pair of simp complexes
#     # return jth row blow of partial_1
#     res =[] 
#     common_edges = my_intersection(pair[0].edges, pair[1].edges)
    
#     if type(j)==int: # First the case when j is an int
#         Kj = partition[j]
#         if Kj in pair:  # if the intersection with Kj is not empty
#             for e in common_edges:
#                 l = [0 for i in range(0, len(Kj.edges))]
#                 for i in range(0, len(Kj.edges)):
#                     if e == Kj.edges[i]:
#                         if pair[0]==Kj:
#                             l[i]=1
#                         if pair[1]==Kj:
#                             l[i]=-1
#                 res +=[l]
#         else: # if the intersection with Kj is empty return 0
#             res += [[0 for i in range(0, len(Kj.edges))] for k in range(0, len(common_edges))]
#         return res
#     elif type(j)==list and len(j)==2: # Second, the case when j is a 2-element set 
#         common_vertices = my_intersection(pair[0].vertices, pair[1].vertices)
#         #for K in partition:
#             #res +=[[0 for i in range(0, len(common_vertices))] for T in K.triangles]
#             #print res
#         if pair == (partition[j[0]], partition[j[1]]):
#             for e in common_edges:
#                 l = [0 for i in range(0, len(common_vertices))]
#                 for i in range(0, len(common_vertices)):
#                     if common_vertices[i]==e[0]:
#                         l[i]=-1
#                     elif common_vertices[i]==e[1]:
#                         l[i]=1
#                 res +=[l]
#         else:
#             common_vertices = my_intersection(partition[j[0]].vertices, partition[j[1]].vertices)
#             res+=[[0 for i in range(0, len(common_vertices))] for k in range(0, len(common_edges))]
#         return res
            
            
            
                    
# def triangle_derivatice3((alpha, beta, gamma), partition, J): 
    
#     _cols = my_intersection(my_intersection(partition[alpha].vertices, partition[beta].vertices), partition[gamma].vertices)
#     if type(J)==int:
#         return [[0 for i in range(0, len(partition[J].edges))] for v in _cols]
        
#     _rows = my_intersection(partition[J[0]].vertices, partition[J[1]].vertices)
    
#     if type(J)==list and len(J)==2:
#         res =[]
#         if set(J).issubset((alpha, beta, gamma)):                
#             for v in _cols:
#                 l =[0 for i in range(0, len(_rows))]
#                 for i in range(0,len(_rows)):
#                     if _rows[i]==v:
#                         l[i] = (-1)**(sum(J)+1)
#                 res +=[l]
#             return res
#         else:
#             return res + [[0 for i in range(0, len(_rows))] for v in _cols]

# def d1(partition, j): # return the jth block of rows
#     if type(j)==int:
#         Kj = partition[j]
#         A =[]
#         for K in partition:
#             if K==Kj:
#                 A+= triangle_derivative1(Kj)
#             else:
#                 A+= [[0 for i in range(0, len(Kj.edges))] for k in range(0, len(K.triangles))]

#         pairs = intersecting_pairs_at_edges(partition)
#         #print "pairs", pairs
#         for pair in pairs:
#             A+=triangle_derivative2(pair, partition, j)
#         triplets = intersecting_triplets_at_vertices(partition)
#         #print "triplets", triplets
#         for triplet in triplets:
#             A+=triangle_derivatice3(triplet, partition, j)
#         return np.array(A).transpose()
#     if type(j)==list and len(j)==2:
#         J = j
#         A =[]
#         pairs = intersecting_pairs_at_edges(partition)
#         triplets = intersecting_triplets_at_vertices(partition)
#         #print len(triplets)
#         #print len(pairs)
#         common_vertices = my_intersection(partition[j[0]].vertices, partition[j[1]].vertices)
#         for K in partition:
#             A+=[[0 for i in range(0, len(common_vertices))] for T in K.triangles]
#         for pair in pairs:
#             #print triangle_derivative2(pair, partition, J)
#             A+=triangle_derivative2(pair, partition, J)
#         for triplet in triplets:
#             A+=triangle_derivatice3(triplet, partition, J)
#         return np.array(A).transpose()            





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

