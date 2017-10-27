import numpy as np
import sympy as sp
import multiprocessing  as mp
from simplicial_complex import *
from edge_derivative import *

#from cover import *


def my_row_reduction(mat, n): #  returns rank, leftovers  
    mat_rref = sp.Matrix(mat).rref()[0] 
    m = mat.shape[0] # row dimension of mat
    l0 = []
    l1 = []
    for i in range(0, m):
        if sum(map(abs, mat_rref.row(i)[0:n]))==0:
            l1 += [list(mat_rref.row(i))]
        else:
            l0 += [list(mat_rref.row(i))]
            
    return len(l0),  l1


def my_mp(args_list):
    pool = mp.Pool(processes=mp.cpu_count())
    print "----------> number of cores used  ", mp.cpu_count()
    res = [pool.apply_async(my_row_reduction, args = tup).get() for tup in args_list]
    # no more processes added
    pool.close()
    # wait for all work to be completed
    pool.join()
    print "----------> number of results returned ", len(res)
    return res    

def parallel_rank(args_list):
    
    mp_res = my_mp(args_list)
    #print "hello", mp_res
    #print "mmmm", map(lambda x:  x[1][0], mp_res)
    #print "rank", np.linalg.matrix_rank(np.array(map(lambda x:  x[1][0], mp_res)))
    #print "++++++++++++++++++++++++++++"
    #print "parallel processing done"
    #print "mp_res", mp_res

    # concatenate different bottoms
    bottom = []
    for i in range(0, len(mp_res)):
    	bottom += mp_res[i][1]

    #print "bottom", bottom

    if [] in bottom:
        bottom.remove([])
    #print bottom
    if bottom == None:
        return sum(map(lambda x: x[0], mp_res)) 
    bottom_mat = np.array(bottom)
    #print "bottom_mat"
    #print bottom_mat
    return sum(map(lambda x: x[0], mp_res)) + np.linalg.matrix_rank(bottom_mat)


def get_number_of_edges(pair):
    return len(set(pair[0].vertices).intersection(pair[1].vertices))

def parallel_homology(K, partition):
    print "computing homology"

    # def n_(i, partition):
    #     #print sum(len(partition[j].edges) for j in range(0, i+1)) +1
    #     return sum(len(partition[j].edges) for j in range(0, i+1)) + 1


    #last_mat = d0(partition, len(partition)-1) 
    # print "###############"
    # print last_mat
    # last_n = last_mat.shape[1]
    # print "last_n=======================>", last_n-1
    # print "##########################################################"
    # print "##########################################################"
    # print "##########################################################"


    n = sum(len(Ki.edges) for Ki in partition)
    # print  "n ===============>", n
    # print "sum(len(Ki.vertices) for Ki in partition)", sum(len(Ki.vertices) for Ki in partition)
    
    foo =[(d0(partition, i), n) for i in range(0, len(partition))]
    
    # for __i in range(0, len(partition)):
    	
    # 	if __i ==3:
    # 		print "__i", __i
	   #  	#print np.array(foo[__i][0])
	   #  	print my_row_reduction(foo[__i][0], n)
	   #  	print "partition[__i].edges", partition[__i].edges
    #zzzz = np.concatenate(tuple(foo), axis=0).shape
    #print zzzz
    # print "##########################################################"
    # print "##########################################################"
    # print "##########################################################"

 	   
    
    #print [n_(i, partition) for i in range(0, len(partition))]
    #foo += [(last_mat, last_n)] 
    # for i in range(0, len(partition)-1):
    #   print "==========================="
    #   print "i", i
    #   print "edges", partition[i].edges
    #   print "vertices", partition[i].vertices
    #   print  d0(partition, i)
    print "-----> parallel rank computation started"
    rk0 =   parallel_rank(foo)
    print "-----> parallel rank computation done"
    #print "rk0", rk0
    beta0 = sum(len(Ki.vertices) for Ki in partition) -rk0
    print "--> beta0 computed", beta0

    # def n_(i, partition):
    #      return sum(len(partition[j].triangles) for j in range(0, i+1))

    #print "hello"
    n = sum(len(Ki.triangles) for Ki in partition)
    #print "here is n", n
    foo = [(d1(partition, i), n) for i in range(0, len(partition))]

    #print "foo", foo

    print "-----> parallel rank computation started"
    rk1 = parallel_rank(foo)
    print "-----> parallel rank computation done"
    
    number_of_edges =  sum(len(Ki.edges) for Ki in partition) + sum(map(get_number_of_edges, intersecting_pairs_at_vertices(partition)))
    beta1 =number_of_edges- rk0 - rk1
    print "--> beta1 computed =", beta1

    return [beta0, beta1]



def main():


  K = simplicialcomplex([["0", "1", "2", "3", "4", "5", "6"],
                        [("0", "1"), ("1", "2"), ("2", "3"), ("0", "3"),
                         ("3", "4"), ("0", "4"), ("4", "5"), ("5", "6"), ("2", "6")], [("0", "3", "4")]])



  K0 = simplicialcomplex([["0", "3", "4"], [("0", "3"), ("3", "4"), ("0", "4")], [("0", "3", "4")]])
  K1 = simplicialcomplex([["1", "2"], [("1", "2")]])
  K2 = simplicialcomplex([["5", "6"], [("5", "6")]])
  K3 = simplicialcomplex([["0", "1", "2", "3", "4", "5", "6"], 
    [("0", "1"),  ("2", "3"), ("2", "6"),("4", "5")]])

  partition = [K0, K1, K2, K3]


  K = simplicialcomplex([["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
                          [("0", "1"), ("1", "2"), ("0", "2"),
                           
                           ("2", "3"), ("3", "4"), ("1", "4"), 
                           
                           ("4", "6"), ("4", "5"), ("5", "6"),
                           ("4", "3"), ("3", "6"),("3", "5"),
                           
                           ("5", "9"), ("6", "7"), 
                           
                           ("7", "8"), ("7", "9"), ("8", "9")
                          ], 
                          [("0", "1", "2"),("3", "4", "5"), ("3", "4", "6"),
                            ("4", "5", "6"), ("3", "5", "6"), ("7", "8", "9")],
                          [("3", "4", "5", "6")]])


  # Example 2
  K0 = simplicialcomplex([["0", "1", "2"], [("0", "1"), ("1", "2"), ("0", "2")], [("0", "1", "2")]])
  K1 = simplicialcomplex([["3", "4", "5", "6"], 
                          [("4", "6"), ("4", "5"), ("5", "6"),
                           ("4", "3"), ("3", "6"),("3", "5")],
                          [("3", "4", "5"), ("3", "4", "6"),
                            ("4", "5", "6"), ("3", "5", "6")],
                         [("3", "4", "5", "6")]])
  K2 = simplicialcomplex([["7", "8", "9"], [("7", "8"), ("7", "9"), ("8", "9")], [("7", "8", "9")]])
  K3 = simplicialcomplex([["1", "2", "3", "4", "5", "6", "7", "9"], 
      [("1", "4"),  ("2", "3"), ("6", "7"),("5", "9")]])

  partition = [K0, K1, K2, K3]
  # print "here"
  # print d0(partition, len(partition)-1).shape
  # print "here 0"
  # print d0(partition, 0)
  # print "here 1"
  # print d0(partition, 1)
  # print "here 2"
  # print d0(partition, 2)
  # print "here 3"
  # print d0(partition, 3
  
  parallel_homology(K, partition)

  #print parallel_rank([(np.array([[ 1],[ 1], [-1]]), 1), 
  #  (np.array([[0]]), 1), (np.array([[0]]), 1), 
  #  (np.array([[0],[0],[0],[0]]), 1)])

  #print  parallel_rank([(np.array([[ 1],[ 1],[-1]]), 1)])


  #zz = (d0(partition, 0), d0(partition, 1), d0(partition, 2), d0(partition, 3))
  #zzzz = np.concatenate(zz, axis=0)
  #print d0(partition, 0)
  #print (d0(partition, 1))
  #print zzzz
  #print "rank", np.linalg.matrix_rank(zzzz)
  #print sum(len(Ki.vertices) for Ki in partition)
  #print "==============================================="
  #print parallel_rank([(d0(partition, 0), 3), (d0(partition, 1), 9), (d0(partition, 2), 12), (d0(partition, 3), 16)])
  #print sum(len(Ki.vertices) for Ki in partition)
  #print [np.linalg.matrix_rank(z_) for z_ in zz]
  #print "d0(partition, 3)"
  #print d0(partition, 3)
  #print "after my_row_reduction"
  #print my_row_reduction(d0(partition, 3), 9)
  #print sp.Matrix(zz[3]).rref()
  #print d0(partition, 3)
if __name__ == '__main__':
    main()
