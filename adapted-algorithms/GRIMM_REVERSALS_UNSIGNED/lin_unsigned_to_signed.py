#!/usr/bin/python                                                                                                             
import sys
import networkx as nx
import copy
from networkx.algorithms.approximation import clique
from networkx.utils.decorators import *

#encontra todas as cliques de um grafo
def find_cliques(G):
    # Cache nbrs and find first pivot (highest degree)
    maxconn=-1
    nnbrs={}
    pivotnbrs=set() # handle empty graph
    for n,nbrs in G.adjacency_iter():
        nbrs=set(nbrs)
        nbrs.discard(n)
        conn = len(nbrs)
        if conn > maxconn:
            nnbrs[n] = pivotnbrs = nbrs
            maxconn = conn
        else:
            nnbrs[n] = nbrs
    # Initial setup
    cand=set(nnbrs)
    smallcand = set(cand - pivotnbrs)
    done=set()
    stack=[]
    clique_so_far=[]
    # Start main loop
    while smallcand or stack:
        try:
            # Any nodes left to check?
            n=smallcand.pop()
        except KeyError:
            # back out clique_so_far
            cand,done,smallcand = stack.pop()
            clique_so_far.pop()
            continue
        # Add next node to clique
        clique_so_far.append(n)
        cand.remove(n)
        done.add(n)
        nn=nnbrs[n]
        new_cand = cand & nn
        new_done = done & nn
        # check if we have more to search
        if not new_cand:
            if not new_done:
                # Found a clique!
                yield clique_so_far[:]
            clique_so_far.pop()
            continue
        # Shortcut--only one node left!
        if not new_done and len(new_cand)==1:
            yield clique_so_far + list(new_cand)
            clique_so_far.pop()
            continue
        # find pivot node (max connected in cand)
        # look in done nodes first
        numb_cand=len(new_cand)
        maxconndone=-1
        for n in new_done:
            cn = new_cand & nnbrs[n]
            conn=len(cn)
            if conn > maxconndone:
                pivotdonenbrs=cn
                maxconndone=conn
                if maxconndone==numb_cand:
                    break
        # Shortcut--this part of tree already searched
        if maxconndone == numb_cand:
            clique_so_far.pop()
            continue
        # still finding pivot node
        # look in cand nodes second
        maxconn=-1
        for n in new_cand:
            cn = new_cand & nnbrs[n]
            conn=len(cn)
            if conn > maxconn:
                pivotnbrs=cn
                maxconn=conn
                if maxconn == numb_cand-1:
                    break
        # pivot node is max connected in cand from done or cand
        if maxconndone > maxconn:
            pivotnbrs = pivotdonenbrs
        # save search status for later backout
        stack.append( (cand, done, smallcand) )
        cand=new_cand
        done=new_done
        smallcand = cand - pivotnbrs

#Funcao que auxilia em obter uma clique maximal
def make_max_clique_graph(G,create_using=None,name=None):
    cliq=list(map(set,find_cliques(G)))
    if create_using:
        B=create_using
        B.clear()
    else:
        B=nx.Graph()
    if name is not None:
        B.name=name

    for i,cl in enumerate(cliq):
        B.add_node(i+1)
        for j,other_cl in enumerate(cliq[:i]):
            # if not cl.isdisjoint(other_cl): #Requires 2.6
            intersect=cl & other_cl
            if intersect:     # Not empty
                B.add_edge(i+1,j+1)
    return B

#encontra todos os 2-ciclos de uma permutacao
def get_two_cycles(blackg, position, permutation, n):
    two_cyclesb = []
    two_cyclesg = []
    
    for edge_i in blackg.edges():
        black11 = edge_i[0]
        black12 = edge_i[1]
        
        gray11 = edge_i[0]
        gray1_2 = []
        
        gray21 = edge_i[1]
        gray2_2 = []
        
        if black11 < n+1:
            if abs(position[black11] - position[black11 + 1]) != 1:
                gray1_2.append(black11 + 1)
        if black11 > 0:
            if abs(position[black11] - position[black11 - 1]) != 1:
                gray1_2.append(black11 - 1)
        if black12 < n+1:
            if abs(position[black12] - position[black12 + 1]) != 1:
                gray2_2.append(black12 + 1)
        if black12 > 0:
            if abs(position[black12] - position[black12 - 1]) != 1:
                gray2_2.append(black12 - 1)
        
        for gray12 in gray1_2:
            for gray22 in gray2_2:
                if gray12 != gray22 and abs(position[gray12] - position[gray22]) == 1:
                    if abs(gray12 - gray22) != 1:
                        node1=[min(black11, black12),max(black11, black12)]
                        node2=[min(gray12, gray22),max(gray12, gray22)]
                        node3=[min(gray11, gray12),max(gray11, gray12)]
                        node4=[min(gray21, gray22),max(gray21, gray22)]
                        new2cycleb = [node1, node2]
                        new2cycleg = [node3, node4]
                        
                        new2cycleb.sort()
                        new2cycleg.sort()
                        
                        if new2cycleb not in two_cyclesb:
                            two_cyclesb.append(new2cycleb)
                            if new2cycleg not in two_cyclesg:
                                two_cyclesg.append(new2cycleg)
                            else : 
                                return "error!"
        
    return two_cyclesb, two_cyclesg 


#encontra todos os 3-ciclos de uma permutacao
def get_three_cycles(blackg, position, permutation, n):
    three_cyclesb = []
    three_cyclesg = []
    
    for edge_i in blackg.edges():
        black11 = edge_i[0]
        black12 = edge_i[1]
        
        gray11 = edge_i[0]
        gray1_2 = []
        
        gray21 = edge_i[1]
        gray2_2 = []
        
        if black11 < n+1:
            if abs(position[black11] - position[black11 + 1]) != 1:
                gray1_2.append(black11 + 1)
        if black11 > 0:
            if abs(position[black11] - position[black11 - 1]) != 1:
                gray1_2.append(black11 - 1)
        if black12 < n+1:
            if abs(position[black12] - position[black12 + 1]) != 1:
                gray2_2.append(black12 + 1)
        if black12 > 0:
            if abs(position[black12] - position[black12 - 1]) != 1:
                gray2_2.append(black12 - 1)
        
        for gray12 in gray1_2:
            for gray22 in gray2_2:
                black21 = gray12
                black2_2 = []
                
                black31 = gray22
                black3_2 = []
                
                if position[black21] < n+1:
                    if abs(black21 - permutation[position[black21]+1]) != 1:
                        black2_2.append(permutation[position[black21]+1])
                if position[black21] > 0:
                    if abs(black21 - permutation[position[black21]-1]) != 1:
                        black2_2.append(permutation[position[black21]-1])
                if position[black31] < n+1:
                    if abs(black31 - permutation[position[black31]+1]) != 1:
                        black3_2.append(permutation[position[black31]+1])
                if position[black31] > 0:
                    if abs(black31 - permutation[position[black31]-1]) != 1:
                        black3_2.append(permutation[position[black31]-1])
                        
                for black22 in black2_2:
                    for black32 in black3_2:
                        if not (min(black21,black22) == min(black31,black32) and max(black21,black22) == max(black31,black32)) :
                            if abs(black22 - black32) == 1 and abs(position[black22] - position[black32]) != 1:                               
                                node1=[min(black11, black12),max(black11, black12)]
                                node2=[min(black21, black22),max(black21, black22)]
                                node3=[min(black31, black32),max(black31, black32)]
                                node4=[min(gray11, gray12),max(gray11, gray12)]
                                node5=[min(gray21, gray22),max(gray21, gray22)]
                                node6=[min(black22, black32),max(black22, black32)]
                                
                                new3cycleb=[node1, node2, node3]
                                new3cycleg=[node4, node5, node6]
                                new3cycleb.sort()
                                new3cycleg.sort()
                                if new3cycleb not in three_cyclesb:
                                    three_cyclesb.append(new3cycleb)
                                    if new3cycleg not in three_cyclesg:
                                        three_cyclesg.append(new3cycleg)
                                    else : 
                                        return "error!"
                
    return three_cyclesb, three_cyclesg 




if __name__ == "__main__" :
    permutation = eval("[%s]" % sys.argv[1])

    n = len(permutation)

    permutation = [0] + permutation + [n+1]
    position    = [-1 for i in range(0, n+2)]


    for i in range(0, n+2) :
        position[permutation[i]] = i

    one_cycles  = []
    two_cycles = []
    three_cycles = []
    long_cycles = []

    blackg = nx.Graph()
    cyclegraph = nx.Graph()
    blackg.add_nodes_from([0,n+1])

    for i in range(0,n+1) :
        if abs(permutation[i] - permutation[i+1]) != 1:
            #se a diferenca entre dois elementos vizinhos eh diferente de um, adiciona ao grafo
            blackg.add_edge(permutation[i], permutation[i+1], nodetype = 1)
        else :
            #senao, eh um 1-ciclo e nao deve ser adicionado ao grafo
            one_cycles.append([permutation[i],permutation[i+1]]) 

    #pega todos os 2-ciclos do grafo de ciclos da permutacao
    two_cb, two_cg = get_two_cycles(blackg, position, permutation, n)
    
    #pega todos os 3-ciclos do grafo de ciclos da permutacao
    three_cb, three_cg = get_three_cycles(blackg, position, permutation, n)
    
    ## Constroi um grafo com todos os 2-ciclos e 3-ciclos para,
    ## com ajuda da clique, retirar um conjunto maximal
    all23_cyclesb = two_cb + three_cb
    all23_cycleslist = copy.deepcopy(all23_cyclesb)
    all23_cyclesg = two_cg + three_cg
    
    for i in range(0,len(all23_cyclesb)):
        all23_cyclesb[i][0] = "(%s,%s)" % (all23_cycleslist[i][0][0], all23_cycleslist[i][0][1])
        all23_cyclesb[i][1] = "(%s,%s)" % (all23_cycleslist[i][1][0], all23_cycleslist[i][1][1])
        
        all23_cyclesg[i][0] = "(%s,%s)" % (all23_cyclesg[i][0][0], all23_cyclesg[i][0][1])
        all23_cyclesg[i][1] = "(%s,%s)" % (all23_cyclesg[i][1][0], all23_cyclesg[i][1][1])
        if len(all23_cyclesb[i]) == 3:
            all23_cyclesb[i][2] = "(%s,%s)" % (all23_cycleslist[i][2][0], all23_cycleslist[i][2][1])
            all23_cyclesg[i][2] = "(%s,%s)" % (all23_cyclesg[i][2][0], all23_cyclesg[i][2][1])
        
         

    
    cyclegraph.add_nodes_from(range(0,len(all23_cyclesb)))
    for i in range(0,len(all23_cyclesb)):
        for j in range(i+1,len(all23_cyclesb)):
            if list(set(all23_cyclesb[i]) & set(all23_cyclesb[j])) != []:
                cyclegraph.add_edge(i,j)
            if list(set(all23_cyclesg[i]) & set(all23_cyclesg[j])) != []:
                cyclegraph.add_edge(i,j)
                
    ## Pega o complemento do grafo, uma vez que se pegarmos uma clique maximal 
    ## de 2,3-ciclos no complemento, significa que eles sao independentes com 
    ## relacao a suas arestas. Com o complemento, procuramos uma clique maximal.
    cycle_graph_inv = nx.complement(cyclegraph)
    
    result=list(map(set,find_cliques(cycle_graph_inv)))
    
    
    ## Se retornou um conjunto maximal, pega os ciclos deste conjunto
    ## e adiciona na lista final de ciclos do grafo da permutacao,
    ## separando entre 2-ciclos e 3-ciclos
    
    finalcycles = []
    if result != []:
        finalcycles = list(max(result,key=len))
    
    
    for finalcycle in finalcycles:
        cycleaux = []
        if len(all23_cycleslist[finalcycle]) == 2:
            cycleaux.append(all23_cycleslist[finalcycle][0][0])
            
            if abs(all23_cycleslist[finalcycle][1][0] - cycleaux[-1]) == 1:
                cycleaux.append(all23_cycleslist[finalcycle][1][0])
                cycleaux.append(all23_cycleslist[finalcycle][1][1])
            else :
                cycleaux.append(all23_cycleslist[finalcycle][1][1])
                cycleaux.append(all23_cycleslist[finalcycle][1][0])
                
            cycleaux.append(all23_cycleslist[finalcycle][0][1])
            
            two_cycles.append(cycleaux)
            
        elif len(all23_cycleslist[finalcycle]) == 3:
            cycleaux.append(all23_cycleslist[finalcycle][0][0])
            if abs(all23_cycleslist[finalcycle][1][0] - cycleaux[-1]) == 1:
                cycleaux.append(all23_cycleslist[finalcycle][1][0])
                cycleaux.append(all23_cycleslist[finalcycle][1][1])
            else :
                cycleaux.append(all23_cycleslist[finalcycle][1][1])
                cycleaux.append(all23_cycleslist[finalcycle][1][0])
            
            if abs(all23_cycleslist[finalcycle][2][0] - cycleaux[-1]) == 1 and abs(all23_cycleslist[finalcycle][2][1] - all23_cycleslist[finalcycle][0][1]) == 1:
                cycleaux.append(all23_cycleslist[finalcycle][2][0])
                cycleaux.append(all23_cycleslist[finalcycle][2][1])
            else :
                cycleaux.append(all23_cycleslist[finalcycle][2][1])
                cycleaux.append(all23_cycleslist[finalcycle][2][0])
                
            cycleaux.append(all23_cycleslist[finalcycle][0][1])
            
            three_cycles.append(cycleaux)
        else :
            print "Error"

    ## Agora temos uma lista de 1-ciclos, uma de 2-ciclos e uma de
    ## 3-ciclos. Gulosamente vamos criar os demais itens com as arestas 
    ## restantes. Como qualquer aresta cinza pode ser utilizada uma unica
    ## vez, vamos salvar em available[i] se a aresta (i, i+1) ja foi utilizada.

    gray_available     = [1 for i in range(0, n+1)]
    black_available    = [1 for i in range(0, n+1)]

    for cycle in one_cycles :
        gray_edge = min(cycle[0], cycle[1])
        black_edge = min(position[cycle[0]], position[cycle[1]])
        gray_available [gray_edge]  = gray_available[gray_edge]  - 1   
        black_available[permutation[black_edge]] = black_available[permutation[black_edge]] - 1


    for cycle in two_cycles :
        gray_edge  = min(cycle[0], cycle[1])
        black_edge = min(position[cycle[1]], position[cycle[2]])
        gray_available[gray_edge]  = gray_available[gray_edge] - 1
        black_available[permutation[black_edge]] = black_available[permutation[black_edge]] - 1

        gray_edge  = min(cycle[2], cycle[3])
        black_edge = min(position[cycle[3]], position[cycle[0]])
        gray_available[gray_edge]   = gray_available[gray_edge] - 1
        black_available[permutation[black_edge]] = black_available[permutation[black_edge]] - 1

    for cycle in three_cycles :
        gray_edge  = min(cycle[0], cycle[1])
        black_edge = min(position[cycle[1]], position[cycle[2]])
        gray_available[gray_edge]  = gray_available[gray_edge] - 1
        black_available[permutation[black_edge]] = black_available[permutation[black_edge]] - 1

        gray_edge  = min(cycle[2], cycle[3])
        black_edge = min(position[cycle[3]], position[cycle[4]])
        gray_available[gray_edge]   = gray_available[gray_edge] - 1
        black_available[permutation[black_edge]] = black_available[permutation[black_edge]] - 1

        gray_edge  = min(cycle[4], cycle[5])
        black_edge = min(position[cycle[5]], position[cycle[0]])
        gray_available[gray_edge]   = gray_available[gray_edge] - 1
        black_available[permutation[black_edge]] = black_available[permutation[black_edge]] - 1


    for i in range(0, n+1) :
        if gray_available[i] :
            start     = i

            cycle = [start]
            end   = start
            while True :
                ## Gray edge
                if end < n+1 and gray_available[end] :
                    gray_available[end] = gray_available[end] - 1
                    end = end + 1
                    cycle.append(end)
                else :
                    gray_available[end-1] = gray_available[end-1] - 1
                    end = end - 1          
                    cycle.append(end)

                ## Black edge
                next_end = None
                if end < n+1 and black_available[end] :
                    next_end = permutation[position[end]+1]
                    black_available[end] = black_available[end] - 1
                else :
                    next_end = permutation[position[end]-1]
                    black_available[next_end] = black_available[next_end] - 1

                if next_end == start :
                    break
                else :
                    cycle.append(next_end)
                    end = next_end
                
            long_cycles.append(cycle)

        
    ## Retorna a lista final de ciclos    
    #print one_cycles + two_cycles + three_cycles + long_cycles


    ########################################
    ########## Unsigned to Signed ##########
    ########################################

    all_cycles = one_cycles + two_cycles + three_cycles + long_cycles
    all_cycles.sort()

    # signed_permutation = [-1 for i in range(0, 2*(n+1))]
    # signed_permutation[0]     = [0]
    # signed_permutation[2*n+1] = -n+1

    signed_permutation = ["Nope" for i in range(0, n+2)]


    for cycle in all_cycles :
        for i in range(len(cycle)/2) :

            if cycle[2*i] > cycle[2*i+1] :
                triple = [ cycle[2*i-1 % len(cycle)], -cycle[2*i], cycle[2*i+1]]
                triple.reverse()
        
            ## signed gray edge goes from i to -(i+1)
    #        if triple[0] > triple[1] :
                triple[0] = -triple[0]
            else :
                triple = [cycle[2*i], -cycle[2*i+1], cycle[ 2*(i+1) % len(cycle)] ]

        

            if position[abs(triple[1])] == position[triple[2]] + 1 :
                signed_permutation[position[abs(triple[1])]] = -triple[1]
    #            print("Triple", triple, -triple[1])
            elif position[abs(triple[1])] == position[triple[2]] - 1 :
                signed_permutation[position[abs(triple[1])]] = triple[1]
    #            print("Triple", triple, triple[1])
            else :
                print("ERRO")

    print str(signed_permutation[1:-1]).replace(" ","").replace("[","").replace("]","")        

    #        print(triple)
