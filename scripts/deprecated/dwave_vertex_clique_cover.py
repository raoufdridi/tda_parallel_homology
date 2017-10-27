from qdk import *
import networkx as nx


def dwave_coloring(G, n, solver='local', url = "https://qubist.dwavesys.com/sapi/", token = "4a1edf3f26f2e227784861af0a0c8588b88f787c" ):
    CG = nx.complement(G)
    print "-----> Qubo construction"
    new_builder = QuadraticBinaryPolynomialBuilder()
    new_builder.AddConstantTerm(len(G.nodes()))
    for _i in range(1, len(G.nodes())+1):
        for _j in range(1, n+1):
            new_builder.AddTerm(-2, int(str(_i) + str(_j)))

    for _i in range(0, len(G.nodes())):
        for _j1 in range(1, n+1):
            for _j2 in range(1, n+1):
                new_builder.AddTerm(1, int(str(_i+1) + str(_j1)), int(str(_i+1) + str(_j2)))


    for _i in range(0, len(G.nodes())):
        for _j in range(0, len(G.nodes())):
            if (G.nodes()[_i], G.nodes()[_j]) in CG.edges():
                #print (G.nodes()[_i], G.nodes()[_j])
                for _k in range(1, n+1):
                    new_builder.AddTerm(1, int(str(_i+1) + str(_k)), int(str(_j+1) + str(_k)))
            

    Q = new_builder.BuildPolynomial()
    print "-----> Qubo constructed"
    
    if solver =='dwave':
        remote_key = ConnectionKey(url, token)
        # Create a remote solver
        print "dwave called: create a remote solver"
        dwave_remote_solver = DWaveSolver(remote_key)

        # Solve the problem and save the results in SolutionList
        # D-Wave solver uses Histogram as default setting and it returns multiple solutions
        dwave_solution = dwave_remote_solver.Minimize(Q)
        print "# of solutions returned", dwave_solution.GetSolutionCount()  
        print "energy", dwave_solution.PeekMinimumEnergySolution().energy
        return dwave_solution.PeekMinimumEnergySolution().configuration

    elif solver =='local':
        print "local solver called"
        # Create a local connection key for D-Wave solver
        local_key = ConnectionKey()
        # Create a local solver and test local server
        dwave_local_solver = DWaveSolver(local_key)

        # Modify some solver parameters
        # Set num_reads to 50 in this example
        # so we are expecting 50 solutions to be returned by D-Wave solver
        dwave_local_solver.num_reads = 50
        dwave_local_solver.answer_mode = "histogram"
        # We also set min_solver_calls and max_solver_calls for embedding solver
        dwave_local_solver.min_solver_calls = 1
        dwave_local_solver.max_solver_calls = 10
        
        solution_list = dwave_local_solver.Minimize(Q)
        print "# of solutions returned", solution_list.GetSolutionCount()
        return solution_list.PeekMinimumEnergySolution().configuration
    else:
        return ("solver not recognized, choose solver ='local' or solver ='dwave'")
        
# def get_clique_cover(dwave_res, G, n):
# 	# take a dwave_coloring which is a dict and returns the actual vertex clique cover
#     cover = dict({})
#     for j in range(0, n):
#         cover[j] = []
#     for i in range(0, len(G.nodes())):
#         for j in range(0, n):
#             if dwave_res[int(str(i+1) + str(j+1))]:
#                         #print  int(str(i+1) + str(j+1))
#                         cover[j] += [G.nodes()[i]]
#     return cover

def get_clique_cover(dwave_res):
    # take a dwave_coloring which is a dict and returns the actual vertex clique cover
    return dwave_res[0].values()

def main():
	n = 3
	G = nx.Graph([('1', '0'),('1', '2'), ('0', '3'),('0', '4'), ('3', '2'), ('3', '4'),
              ('2', '6'), ('5', '4'), ('5', '6')])
	print "G.edges()", G.edges()
	dres = dwave_coloring(G, n)
	print "cliques", get_clique_cover(dres, G, n)

if __name__ == '__main__':
    main()
