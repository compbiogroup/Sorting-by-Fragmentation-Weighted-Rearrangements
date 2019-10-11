#!/usr/bin/python2.6
# -*- coding: iso-8859-1 -*-

 #   This software was developed by Zanoni Dias, Ulisses Dias
 #
 #   It should not be redistributed or used for any commercial purpose
 #   without written permission from authors
 #
 #   release date: nov 15, 2011
 #
 # This software is experimental in nature and is
 # supplied "AS IS", without obligation by the authors to provide
 # accompanying services or support.  The entire risk as to the quality
 # and performance of the Software is with you. The authors
 # EXPRESSLY DISCLAIM ANY AND ALL WARRANTIES REGARDING THE SOFTWARE,
 # WHETHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO WARRANTIES
 # PERTAINING TO MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE.
 #
 #

 # If you use this softwore anytime in your work, please cite the
 # following paper:
 #
 # DIAS, U. ; DIAS, Z. . Extending Bafna-Pevzner algorithm. In:
 # International Symposium on Biocomputing (ISB'2010), 2010, Calicut,
 # Kerala. Proceedings of the 1st International Symposium on
 # Biocomputing (ISB'2010). New York, NY, USA : ACM, 2010. p. 1-8.

import sys
import copy
import math

sys.setrecursionlimit(2000)
class dias2010 :
    def __init__(self, param_permutation) :
        self.input = param_permutation
        aux =  param_permutation.split(",")
        permutation = []
        for item in aux :
            permutation.append(int(item))
        self.graph = cycle_graph(permutation)

    def is_reversal(self, permutation) :
        size = len(permutation)
        for i in range(size) :
            if int(permutation[i]) != ((size -(i + 1)) % size) + 1 :
                return False
        return True

    def analyze_transposition(self, cycle_graph, i,j,k) :
        inner_graph = copy.deepcopy(cycle_graph)
        inner_graph.transposition(i, j, k)
        next_step = self.sort_steps(inner_graph, transposition = False)
        return next_step

    def fw_t(self, i, j, k, size):
        if (i == 1 and k == size+1):
            return 1;
        elif (i == 1 or k == size+1):
            return 2;
        else:
            return 3;

    def sort(self) :
        distance = 0
        sequence = []
        self.trace = ""
        graph = self.graph
        while not graph.is_ordered() :#
            try :
                distance = distance + 1
                (i1,j1,k1) = self.sort_steps(graph)
                i = min(i1, j1, k1)
                k = max(i1, j1, k1)
                j = (i1 + j1 + k1) - i - k
                sequence.append([i,j,k])
                graph.transposition(i,j,k)
            except :
                print "Erro %s" % graph.__str__()
                print "real-bafna-pevzner - %s - %i - %s" % (self.input, distance, sequence)
                print(graph)
                sys.exit()

        #print "real-bafna-pevzner - %s - %i - %s" % (self.input, distance, sequence)

        res = open(sys.argv[2], "a")
        sor = open(sys.argv[3], "a")
        print >> sor, ("%s" % str(sequence).replace(" ",""))
        weight = 0
        for t in sequence:
            weight += self.fw_t(t[0],t[1],t[2],self.graph.n)
        print >> res, ("%d" % weight)
        print(self.graph.n)

        #print len(sequence),
        #print(sequence)

    def sort_steps(self, cycle_graph, transposition = True) :
        # Oriented cycle
        cycle = cycle_graph.get_oriented_cycle()
        if cycle :
            if cycle.tcycle :
                (i,j,k) = cycle_graph.find_oriented_triple(cycle)
                if  i != 0  :
                    return i.index, j.index, k.index
                else :
                    (y, z, x) = cycle_graph.find_oriented_triple(cycle, zero_move = True)
                    a = z.rac.ab
                    b = z.ap.ac
                    if b.index < a.index :
                        return (b.index, a.index, z.index)
                    else :
                        return (b.index, z.index, x.index)

        cycle = cycle_graph.get_long_cycle()
        if cycle :
            (i,j,k) = cycle_graph.shuffling_transposition()
            if i and j and k :
                self.trace = self.trace + "12,"
                return (i.index, j.index, k.index)

            (i,j,k) = cycle_graph.no_shuffling_transposition(cycle)
            if i and j and k :
                self.trace = self.trace + "13,"
                return (i.index, j.index, k.index)

        # There is only 2-cycles and 1-cycles on G(pi)
        (i,j,k) = cycle_graph.two_cycles_transposition()
        if i and j and k :
            self.trace = self.trace + "14,"
            return (i.index, j.index, k.index)

class cycle_graph :
    def __init__(self, permutation) :
        n = len(permutation)
        self.n = n
        self.permutation = permutation
        node_list_value = [-1 for x in range(n+2)]
        node_list_index = [-1 for x in range(n+2)]

        # Lemma 9: creating ap and ab
        previous_node = cycle_graph_node(0,0)
        node_list_value[0] = previous_node
        node_list_index[0] = previous_node

        for i in range(n) :
            local_node = cycle_graph_node(i+1, int(permutation[i]))
            node_list_value[int(permutation[i])] = local_node
            node_list_index[i+1] = local_node
            previous_node.set_pointers(ab = local_node)
            local_node.set_pointers(ap = previous_node)
            previous_node = local_node

        local_node = cycle_graph_node(n+1, n+1)
        node_list_value[n+1] = local_node
        node_list_index[n+1] = local_node
        previous_node.set_pointers(ab = local_node)
        local_node.set_pointers(ap = previous_node)

        # Lemma 10: creating ac
        for i in range(n+1) :
            node = node_list_value[i]
            node.ac = node_list_value[node.value + 1]
            node.ac.rac = node

        self.begin_index = node_list_index[0]
        self.end_index = node_list_index[-1]
        self.begin_value = node_list_value[0]
        self.end_value = node_list_value[-1]

        self.decompose_cycles(node_list_index)

    def decompose_cycles(self, node_list_index) :
        def is_oriented(cycle) :
            previous = cycle[0]
            for count in range(1,len(cycle)) :
                if previous < cycle[count] :
                    return 1
                previous = cycle[count]
            return 0

        n = self.n
        self.clean_visit()
        # Theorem 5: decomposing cycles
        cycles = self.get_cycles()

        for i in range(len(cycles)) :
            cycle = cycles[i]
            ccycle = len(cycle)
            tcycle = is_oriented(cycle)
            ncycle = i+1
            cbegin = node_list_index[cycle[-1]]
            cend = node_list_index[cycle[0]]
            for element in cycle :
                node_list_index[element].ccycle = ccycle
                node_list_index[element].tcycle = tcycle
                node_list_index[element].ncycle = ncycle
                node_list_index[element].cbegin = cbegin
                node_list_index[element].cend = cend

    #######################################################################
    ######################## Metodos necessarios ##########################
    #######################################################################
    #ap     : points to the record that stores pi_{i-1}, 1 <= i <= n+1
    #ab     : points to the record that stores pi_{i+1}, 0 <= i <= n
    def transposition(self, i, j, k) :
        node = self.begin_index
        size = self.n + 2
        count = 0
        node_i = 0
        node_j = 0
        node_k = 0
        while node :
            if count == i :
                node_i = node
            if count == j :
                node_j = node
            if count == k :
                node_k = node
            node = node.ab
            count = count + 1

        node_j.ap.ab = node_k
        node_k.ap.ab = node_i
        node_i.ap.ab = node_j

        aux = node_j.ap
        node_j.ap = node_i.ap
        node_i.ap = node_k.ap
        node_k.ap = aux


        node_list_index = []
        node = self.begin_index
        count = 0
        while node:
            node.index = count
            node_list_index.append(node)
            node = node.ab
            count = count + 1

        self.decompose_cycles(node_list_index)

    #######################################################################
    ######################### Metodos auxiliares## ########################
    #######################################################################
    def clean_visit(self) :
        node = self.begin_index
        while node :
            node.visit = 0
            node = node.ab

    def is_ordered(self) :
        node = self.begin_index
        count = 0
        while node :
            if node.value != count :
                return False
            node = node.ab
            count = count + 1
        return True

    def print_nodes(self) :
        if self.begin_index:
            print("begin_index = %i" % self.begin_index.index)
        if self.end_index :
            print("end_index   = %i" % self.end_index.index)

        node = self.begin_index
        while node :
            print(node)
            node = node.ab

    def get_cycles(self) :
        cycles = []
        self.clean_visit()
        n = self.n
        node = self.end_index
        while node.ap :
            cycle = []
            local_node = node
            while not local_node.visit :
                cycle.append(local_node.index)
                local_node.visit = 1
                local_node =  local_node.ap.ac
            if len(cycle) :
                cycles.append(cycle)
            node = node.ap
        return cycles

    def __str__(self) :
        str = ""
        node = self.begin_index
        while node :
            #str = str + "%s\n" % node.__str__()
            str = str + "%s," % node.value
            node = node.ab
        return str

    def get_long_cycle(self) :
        node = self.begin_index

        while node :
            if node.ccycle > 2 :
                return node.cend
            node = node.ab
        return 0

    def get_long_non_oriented_cycle(self) :
        node = self.begin_index
        while node :
            if node.ccycle > 2 and not node.tcycle :
                return node.cend
            node = node.ab
        return 0

    def get_oriented_cycle(self) :
        node = self.end_index
        while node :
            if node.ccycle > 2 and node.tcycle   :
                return node.cend
            node = node.ap
        return 0


    def get_oriented_cycles(self) :
        cycles = []
        self.clean_visit()
        node = self.end_index
        while node :
            if node.ccycle > 2 and node.tcycle and not node.cend.visit  :
                node.visit = 1
                cycles.append(node)
            node = node.ap
        return cycles


    # Number of gray edges that must be traversed to go from r to t
    def distance(self, r, t) :
        count = 0
        node = r
        while (node.index != t.index) :
            count = count + 1
            node = node.ap.ac
        return count

    # Split the cycle in 3 based on the transposition
    # i, j and k must be a triple
    def split_cycle(self, i, j, k) :
        if i.ncycle == j.ncycle == k.ncycle :
            splits = [k,i,j]
            cycles = [[],[],[]]
            for count in range(0,3) :
                node = splits[count]
                while node.index != splits[count+1].index :
                    cycles[count].append(node)
        else :
            return [[],[],[]]


    #######################################################################
    #################### Metodos retirados de lemas #######################
    #######################################################################


    def strongly_oriented_transposition(self, cycle, transposition) :
        breakpoints = self.strongly_oriented_breakpoints(cycle)
        if len(breakpoints) == 3 :
            if not transposition :
                return True
#             # Main Function
#             # Finding right edges
#             (r, i1) = (cycle.cend.rac.ab, cycle.cend)
#             node = cycle.cend.ap.ac
#             (s, t)  = (node.rac.ab, node)
#             while s.index > t.index :
#                 node = node.ap.ac
#                 (s, t)  = (node.rac.ab, node)
#             return self.two_right_edges_transposition(r,i1,s,t)
            else :
                return self.two_right_edges_non_crossed_transposition(breakpoints)

        else :
            if transposition :
                return (0,0,0)
            else :
                return False


    # Lemma 4, 5
    def strongly_oriented_transposition_old(self, cycle, transposition) :
        breakpoints = self.strongly_oriented_breakpoints(cycle)
        if len(breakpoints) == 3 :
            if not transposition :
                return True
            # Main Function
            # Finding right edges
            (r, i1) = (cycle.cend.rac.ab, cycle.cend)
            node = cycle.cend.ap.ac
            (s, t)  = (node.rac.ab, node)
            while s.index > t.index :
                node = node.ap.ac
                (s, t)  = (node.rac.ab, node)
            return self.two_right_edges_transposition(r,i1,s,t)
        else :
            if transposition :
                return (0,0,0)
            else :
                return False

    def two_right_edges_transposition(self,r,i1,s,t) :
        #direction :
        #   0 = Backward
        #   1 = Foreward
        # position : place to put the interval black edges
        def find_interval(node, direction, interval, position) :
            def next_node(node, direction) :
                if direction :
                    return node.ab
                else :
                    return node.ap

            ncycle = node.ncycle
            next = next_node(node, direction)
            while next.ncycle != ncycle :
                if next.tcycle == 0 and next.ccycle > 2 :
                    if not interval.has_key(next.ncycle) :
                        interval[next.ncycle] = [0,0,0]
                        interval[next.ncycle][position] = next
                    else :
                        interval[next.ncycle][position] = next
                next = next_node(next, direction)
            return next

        # Classificando em tipos
        if r.index > s.index :
            #Type 1: looking for r' and t' and internal non-oriented cycles
            interval = {}
            r_linha = find_interval(r, 0, interval, 0)
            t_linha = find_interval(t, 1, interval, 1)

            # Verify strongly crossed cycles
            crossed = False
            keys = interval.keys()
            count = 0
            keys_size = len(keys)
            while not crossed and count < keys_size :
                cycle = interval[keys[count]]
                if cycle[0] and cycle[1] :
                    if cycle[0].index == cycle[0].cbegin.index  :
                        crossed = True
                    elif cycle[1].index == cycle[1].cend.index :
                        crossed = True
                count = count + 1

            if crossed :
                if r_linha.index != s.index :
                #Type 1(a): Lemma 4
                    d_r_t = self.distance(r, t)
                    if d_r_t % 2 != 0 : # d(s,t) is odd => t(s+1,r,i1)
                        return (s.rac.ab, r, i1)
                    else : # d(s,t) is even => t(s,r,i1)
                        return (s, r, i1)
                else :
                    return (s, t, t_linha)
            else :
                return self.two_right_edges_non_crossed_transposition([t_linha, s,r])

        else :
            #type 2: Looking for s', t', a and a'
            interval = {}
            s_linha = find_interval(s, 0, interval, 0)
            t_linha = find_interval(t, 1, interval, 2)
            a = t_linha.ap.ac
            a_linha = find_interval(a, 1, interval, 1)

            # Check for strongly crossed cycles
            crossed = False
            keys = interval.keys()
            count = 0
            keys_size = len(keys)
            while not crossed and count < keys_size :
                cycle = interval[keys[count]]
                if cycle[0] and cycle[1] and cycle[2] :
                    if cycle[0].index == cycle[0].cbegin.index  :
                        crossed = True
                    elif cycle[2].index == cycle[2].cend.index :
                        crossed = True
                count = count + 1

            if crossed :
                d_s_linha_r = self.distance(s_linha, r)
                d_t_a_linha = self.distance(t, a_linha)
                if d_s_linha_r % 2 == d_t_a_linha % 2 :
                    return (r, s, t)
                else :
                    return (s, t, i1)
            else :
                return self.two_right_edges_non_crossed_transposition([t_linha, s,a_linha])
        return (0,0,0)


    def two_right_edges_non_crossed_transposition(self, breakpoints) :
        # Finding right edges
        x = breakpoints[0]
        y = x.ap.ac
        d_x_y = 1

        z = breakpoints[1].ap.ac
        d_y_z = self.distance(y,z)
        d_z_x = self.distance(z,x)
        if d_y_z % 2 == 1 or d_z_x % 2 == 1 :
            return (y, z, x)
        elif z.index != breakpoints[2].index :
            return (y, z.ap.ac, x)
        elif x.index != x.cend.index and y.index != breakpoints[1].index :
            return (y.ap.ac, z, x.rac.ab)
        else :
            return (z.ap.ac,z.rac.ab,z)


    # Lemma 11:
    def strongly_oriented_breakpoints(self, cend_node) :
        def cmp(a,b) :
            return b.index - a.index

        cycle = [cend_node]
        next_node = cend_node.ap.ac
        while next_node.index != cend_node.index :
            cycle.append(next_node)
            next_node = next_node.ap.ac

        size = len(cycle)
        sorted_cycle = list(cycle)
        sorted_cycle.sort(cmp)
        cycle.append("x")
        sorted_cycle.append("x")
        breakpoints = []
        for i in range(size) :
            for j in range(size) :
                if cycle[i] == sorted_cycle[j] and cycle[i+1] != sorted_cycle[j+1] :
                    breakpoints.append(cycle[i])

        return breakpoints

    #Lemma 12: Encontrar dois ciclos entrelacados (i,j,k) e (x,y,z)
    def shuffling_transposition(self) :
        i = self.end_index
        while i.index != 0 :
            if i.ccycle > 2 and i.tcycle == 0 : # long non-oriented cycle {C candidate}
                array_cycle = self.find_shuffling_edges(i)
                for cend in array_cycle.keys() :
                    if len(array_cycle[cend]) == 3 :
                        return array_cycle[cend][2], array_cycle[cend][1], array_cycle[cend][0]
            i = i.ap
        return 0,0,0

    def find_shuffling_edges(self, i) :
        array_cycle = {}
        j = i.ap
        last_visited = i
        while j.index != 0 :
            if j.ncycle == i.ncycle :
                last_visited = j
            elif j.ccycle > 2 and j.tcycle == 0 : # long non-oriented cycle {C' candidate}
                if not array_cycle.has_key(j.cend) :
                    array_cycle[j.cend] = [last_visited]
                elif array_cycle[j.cend][-1].index != last_visited.index :
                    array_cycle[j.cend].append(last_visited)
            j = j.ap
        return array_cycle

    # Lemma 13: (zero_move = False) Finds oriented triple with two odd distances
    def find_oriented_triple(self, oriented_cycle, all = False, zero_move = False) :
        all_triples = []
        k = oriented_cycle.cend
        size = oriented_cycle.ccycle
        while k.ap.ac.index != oriented_cycle.cend.index :
            i = k.ap.ac
            dist_k_i = 1
            while i.ap.ac.index != k.index and i.index != k.index :
                j = i.ap.ac
                dist_i_j = 1
                while j.index != k.index :
                    while ((not (i.index < j.index < k.index and
                                 (zero_move or dist_i_j % 2 == 1
                                  or (oriented_cycle.ccycle-(dist_k_i + dist_i_j)) % 2 == 1))) and
                           j.index != k.index ) :
                        j = j.ap.ac
                        dist_i_j = dist_i_j + 1

                    if (i.index < j.index < k.index and
                        (zero_move or dist_i_j % 2 == 1 or
                         (oriented_cycle.ccycle-(dist_k_i + dist_i_j)) % 2 == 1)) :
                        if all :
                            all_triples.append([i,j,k])
                        else :
                            return (i, j, k)

                        j = j.ap.ac
                        dist_i_j = dist_i_j + 1
                i = i.ap.ac.ap.ac
                dist_k_i = dist_k_i + 2
            k = k.ap.ac
        if all :
            return all_triples
        else :
            return 0,0,0

    # all cycles on graph must be non-oriented
    # begin.index < end.index
    # return (x,y) : (D = (x ... c ... d ... y) such (i1, ik) and (c, d) interleaves
    def find_interleaving_pair(self, begin, end) :
        node = end.ap
        while node.index != begin.index :
            if not node.tcycle :
                if node.index == node.cend.index and node.cbegin.index < begin.index :
                    return (node.cbegin, node.cend)
                if node.index == node.cbegin.index and node.cend.index > end.index :
                    return (node.cbegin, node.cend)
            node = node.ap
        return (0, 0)


    #
    # Dado um ciclo orientado cruzado com um ciclo nao orientado,
    # procura uma tripla que torne o ciclo nao orientado em orientado
    #
    def oriented_crossed_transposition(self, cycle, triples, transposition) :
        array_cycle = self.find_shuffling_edges(cycle.cend)

        for cend in array_cycle.keys() :
            size = len(array_cycle[cend])
            outer_count = size-2
            while outer_count >= 0 :
                (l1,l2,l3,l4) = (0,0,0,0)
                if outer_count == size-2 :
                    l1 = 0
                    l2 = array_cycle[cend][outer_count+1].index
                    l4 = cend.cend.index
                else :
                    l1 = array_cycle[cend][outer_count+2].index
                    l2 = array_cycle[cend][outer_count+1].index
                    l4 = self.end_index.index
                inner_count = outer_count
                while inner_count >= 0 :
                    l3 = array_cycle[cend][inner_count].index
                    for triple in triples :
                        (i,j,k) = triple[0:3]
                        if l1 <= i.index < l2 <= j.index < l3 <= k.index <= l4 :
                            if transposition :
                                return (i, j, k)
                            else :
                                return True
                    inner_count = inner_count - 1
                outer_count = outer_count - 1
        if transposition :
            return (0,0,0)
        else :
            return False


    def oriented_even_transposition(self, cycle, triples, transposition) :
        def cmp(triple1, triple2) :
            return triple2[-1] - triple1[-1]

        if cycle.ccycle % 2 == 0 :
            if not transposition :
                return True

            for triple in triples :
                sum_even = 0
                dist_1 = self.distance(triple[0], triple[1])
                dist_2 = self.distance(triple[1], triple[2])
                dist_3 = self.distance(triple[2], triple[0])
                if dist_1 % 2 == 0 :
                    sum_even = sum_even + dist_1
                if dist_2 % 2 == 0 :
                    sum_even = sum_even + dist_2
                if dist_3 % 2 == 0 :
                    sum_even = sum_even + dist_3
                triple.append(sum_even)
            triples.sort(cmp)
            (i,j,k,w) = triples[0][0:4]
            if w > 2 :
                return i, j, k

            # Encontrando ciclos pares internos
            even_cycles = []
            node = cycle.cend
            while node.index != 0 :
                if node.ncycle != cycle.ncycle and node.ccycle % 2 ==0 :
                    even_cycles.append([node.index])
                    inner_node = node.ap.ac
                    while inner_node.index != node.index :
                        even_cycles[-1].append(inner_node.index)
                        inner_node = inner_node.ap.ac
                node = node .ap

            # Verificando quem sera o mais intercalado
            for triple in triples :
                Cpares = list(even_cycles)
                (i,j,k) = triple[0:3]
                splits = [k,i,j]
                cycles = [[],[],[]]
                for count in range(0,3) :
                    node = splits[count]
                    while node.index != splits[(count+1)%3].index :
                        cycles[count].append(node.index)
                        node = node.ap.ac
                    if len(cycles[count]) % 2 == 0 :
                        Cpares.append(cycles[count])


                weight = 0
                for cycle in cycles :
                    if len(cycle) % 2 != 0 and len(cycle) > 2 :
                        for Cpar in Cpares :
                            Cimpar = list(cycle)
                            Cimpar.sort()
                            count_P = 0 #contador par
                            size_P = len(Cpar)
                            count_I = 0 #contador impar
                            size_I = len(Cimpar)
                            while count_P < size_P and count_I < size_I :
                                if Cpar[count_P] < Cimpar[count_I] :
                                    if Cimpar[count_I] == Cpar[count_P] + 1 :
                                        weight = weight + 1
                                    count_P = count_P + 1
                                else :
                                    if Cpar[count_P] == Cimpar[count_I] + 1 :
                                        weight = weight + 1
                                    count_I = count_I + 1
                triple.append(weight)
            triples.sort(cmp)


            (i,j,k) = triples[0][0:3]
            return i, j, k
        else :
            if transposition :
                return (0,0,0)
            else :
                return False

    def oriented_inner_non_oriented_transposition(self, cycle, triples, transposition) :
        def cmp(triple1, triple2) :
            return triple2[-1] - triple1[-1]

        if len(triples) > 0 :
            if not transposition :
                return True
            #for triple in triples :
            #    triple.append(triple[2].index-triple[0].index)
            #triples.sort(cmp)
            right = [[cycle.cbegin, cycle.cend]]
            left = []
            node = cycle.cend.ap.ac
            while node.index != cycle.cend.index :
                if node.index < node.rac.ab.index :
                    left.append([node.rac.ab, node])
                else :
                    right.append([node.rac.ab, node])
                node = node.ap.ac

            for triple in triples :
                weight = 0
                (i,j,k) = triple[0:3]
                for edge in left :
                    if i.index <= edge[1].index < j.index < edge[0].index <= k.index :
                        weight = weight + 1

                for edge in right :
                    if i.index < edge[0].index <= j.index <= edge[1].index < k.index :
                        weight = weight - 1
                triple.append(weight)
            triples.sort(cmp)

            (i,j,k) = triples[0][0:3]
            return (i,j,k)

        else :
            if transposition :
                return (0,0,0)
            else :
                return False

    def oriented_generic_transposition(self, cycle, triples, transposition) :
        if len(triples) > 0 :
            (i,j,k) = triples[0][0:3]
            return (i, j, k)
        else :
            return (0,0,0)


    def oriented_zero_move_crossed_even_transposition(self, cycle, triples, transposition) :
        for triple in triples :
            (y,z,x) = triple[0:3]
            a = z.rac.ab
            b = z.ap.ac
            even_cycles_transpositions = []
            if self.distance(b,x) % 2 == 0 :
                even_cycles_transpositions.append([a,1,y.index,self.end_index.index])
                even_cycles_transpositions.append([b, 1, y.index, x.index])
            else :
                even_cycles_transpositions.append([a, 1, y.index, x.index])
                even_cycles_transpositions.append([b, 1, y.index,  self.end_index.index])
            even_cycles_transpositions.append([z, 1, x.index, self.end_index.index])
            even_cycles_transpositions.append([y, 1, z.index, self.end_index.index])
            even_cycles_transpositions.append([a, 1, b.index, self.end_index.index])

            for ect in even_cycles_transpositions :
                (i,j,k) = self.moving_even_cycles_transposition([ect[0]],ect[1], ect[2],ect[3])
                if i and j and k :
                    if transposition :
                        return (i, j, k)
                    else :
                        return True
        if transposition :
            return (0,0,0)
        else :
            return False


    def oriented_zero_move_crossed_oriented_transposition1(self, triples_1, triples_2, transposition) :
        (y, z, x) = triples_1[0][0:3]
        a = z.rac.ab
        b = z.ap.ac
        other_cycle_transpositions = []
        if self.distance(b,x) % 2 == 0 :
            other_cycle_transpositions.append([a,1,y.index,self.end_index.index])
            other_cycle_transpositions.append([b, 1, y.index, x.index])
        else :
            other_cycle_transpositions.append([a, 1, y.index, x.index])
            other_cycle_transpositions.append([b, a.index, y.index,  self.end_index.index])
        other_cycle_transpositions.append([z, b.index, x.index, self.end_index.index])
        other_cycle_transpositions.append([y, a.index, z.index, self.end_index.index])
        other_cycle_transpositions.append([a, 1, b.index, x.index])

        for triple in triples_2 :
            (i,j,k) = triple[0:3]
            for oct in other_cycle_transpositions :
                (move,start,through,until) = oct[0:4]
                if start <= i.index < move.index < j.index < through < k.index <= until :
                    if transposition :
                        return (i, j, k)
                    else :
                        return True
        if transposition :
            return (0,0,0)
        else :
            return False


    def oriented_zero_move_crossed_oriented_transposition2(self, triples_1, triples_2, transposition) :
        (y1,z1,x1) = triples_1[0][0:3]
        (y2,z2,x2) = triples_2[0][0:3]

        (a1,b1) = (z1.rac.ab, z1.ap.ac)
        (a2,b2) = (z2.rac.ab, z2.ap.ac)
        transp = []
        if (a1.index < a2.index) :
            transp = [a1,a2,z2]
        elif (a2.index < a1.index) :
            transp = [a2,a1,z1]

        if len(transp) == 3 :
            if transposition :
                return (transp[0], transp[1], transp[2])
            else :
                return True
        else :
            if transposition :
                return (0,0,0)
            else :
                return False

    def oriented_zero_move_generic_transposition(self,cycle, triples, transposition) :
        if not transposition :
            return True
        for triple in triples :
            (y,z,x) = triple[0:3]

            a = z.rac.ab
            b = z.ap.ac
            if b.index < a.index :
                return (b, a, z)
            else :
                return (b, z, x)
        return (0,0,0)


    def find_non_oriented_triples(self) :
        all_triples = []
        k = self.end_index
        while k.ap.index != 0 :
            if k.ccycle % 2 == 0 :
                j = k.ap
                while j.index != 0 :
                    if j.ccycle % 2 == 0 :
                        i = j.ap
                        while i.index != 0 :
                            if not i.tcycle and i.ccycle % 2 == 0 :
                                if not (k.ncycle == j.ncycle == i.ncycle) :
                                    if j.ncycle == k.ncycle  and self.distance(k,j) % 2 == 1 :
                                        all_triples.append([i, j, k])
                                    elif i.ncycle == j.ncycle and self.distance(j,i) % 2 == 1 :
                                        all_triples.append([i, j, k])
                                    elif i.ncycle == k.ncycle and self.distance(k,i) % 2 == 1 :
                                        all_triples.append([i, j, k])
                            i = i.ap
                    j = j.ap
            k = k.ap
        return all_triples

    def classify_non_oriented_shuffling_triples(self, triples) :
        for triple in triples :
            triple.append([])

        node = self.end_index
        self.clean_visit
        while node.index != 0 :
            if not node.tcycle and node.ccycle > 2 and not node.cend.visit :
                node.visit = 1
                for triple in triples :
                    if not (
                        (triple[2].index < node.cbegin.index) or
                        (triple[0].index > node.index) or
                        (triple[2].index > node.index and triple[0].index < node.cbegin.index)) :
                        inner = triple[2].ap
                        found = False
                        while not found and inner.index != triple[1].index :
                            if inner.ncycle == node.ncycle :
                                found = True
                            inner = inner.ap

                        if found :
                            inner = triple[1].ap
                            found = False
                            while not found and inner.index != triple[0].index :
                                if inner.ncycle == node.ncycle :
                                    found = True
                                inner = inner.ap
                            if found :
                                triple[3].append(node)
            node = node.ap
        return triples

    def classify_non_oriented_triples(self, triples) :
        def cmp(triple1, triple2) :
            if len(triple1[-2]) > 0 and  len(triple2[-2]) > 0 :
                return triple2[-1] - triple1[-1]
            if len(triple1[-2]) == 0 and len(triple2[-2]) == 0 :
                return triple2[-1] - triple1[-1]
            return len(triple2[-2]) - len(triple1[-2])

        node = self.end_index
        right = []
        left = []
        while node.index != 0 :
            if node.index < node.rac.ab.index :
                left.append([node.rac.ab, node])
            else :
                right.append([node.rac.ab, node])
            node = node.ap

        for triple in triples :
            weight = 0
            (i,j,k) = triple[0:3]
            for edge in left :
                if i.index < edge[1].index < j.index < edge[0].index < k.index :
                    weight = weight + 2

            for edge in right :
                if i.index < edge[0].index < j.index < edge[1].index < k.index :
                    weight = weight - 1
            triple.append(weight)
        triples.sort(cmp)
        return triples



    def classify_non_oriented_crossing_triples(self, triples) :
        def cmp(triple1, triple2) :
            return triple2[-1] - triple1[-1]

        def classify_interleaved_edges(interleaved, shuffled) :
            count_edges  = []
            node = interleaved.cend.ap
            open = interleaved.cend
            edges = []
            while node.index >= interleaved.cbegin.index :
                if node.ncycle == shuffled.ncycle :
                    edges.append(node)
                elif node.ncycle == interleaved.ncycle :
                    count_edges.append([open,node,edges])
                    open = node
                    edges = []
                node = node.ap
            return count_edges

        crossed =  {}
        for triple in triples :
            if len(triple[3]) > 0 :
                weight = 0
                half = 0
                for shuffled in triple[3] :
                    if not crossed.has_key(shuffled.ncycle) :
                        node = shuffled.cend
                        inner_crossed = {}
                        while node.index != shuffled.cbegin.index :
                            if node.ncycle != shuffled.ncycle and not node.tcycle and node.ccycle > 2 :
                                if not inner_crossed.has_key(node.ncycle) :
                                    inner_crossed[node.ncycle] = classify_interleaved_edges(node, shuffled)
                            node = node.ap
                        crossed[shuffled.ncycle] = inner_crossed

                    (i,j,k) = triple[0:3]
                    for cross in crossed[shuffled.ncycle] :
                        for item in crossed[shuffled.ncycle][cross] :
                            (b,a,c) = item
                            if len(c) > 0 :
                                # retirando aresta
                                if (a.index < i.index < c[-1].index <= c[0].index < j.index < b.index) :
                                    weight = weight - 1

                                # entrelacada com ciclo criado
                                if  j.index < b.index < k.index :
                                    half = 1

                                if i.index < a.index < j.index :
                                    half = 2

                                if half == 1  and i.ncycle == j.ncycle == b.ncycle :
                                    weight = 3

                                if half == 2 and j.ncycle == k.ncycle == b.ncycle :
                                    weight = 3
                            else :
                                if a.index < k.index < b.index :
                                    weight = weight + 3
                                elif i.index < a.index < j.index < b.index:
                                    weight  = weight + 1
                                elif a.index < i.index < b.index < j.index :
                                    weight = weight + 1
                triple.append(weight)
            else :
                triple.append(-10)

        triples.sort(cmp)
        return triples

    # Mover move, passar por through e pesquisar ateh until
    def moving_even_cycles_transposition(self, move, start, through, until) :
        node = self.end_index
        while node.index > until :
            node = node.ap

        after_edges = []
        while node.index > through :
            if node.ccycle % 2 == 0  and not node.tcycle :
                after_edges.append(node)
            node = node.ap

        if len(after_edges) == 0 :
            return (0, 0, 0)

        node = node.ap
        inner_edges = []
        while node.index > move[-1].index :
            if node.ccycle % 2 == 0 and not node.tcycle :
                inner_edges.append(node)
            node = node.ap

        if len(inner_edges) == 0 :
            return (0, 0, 0)

        node = move[0].ap
        while node.index >= start :
            if node.ccycle % 2 == 0 and not node.tcycle :
                i = node
                for j in inner_edges :
                    for k in after_edges :
                        if not (k.ncycle == j.ncycle == i.ncycle) :
                            if j.ncycle == k.ncycle  and self.distance(k,j) % 2 == 1 :
                                return (i, j, k)
                            elif i.ncycle == j.ncycle and self.distance(j,i) % 2 == 1 :
                                return (i, j, k)
                            elif i.ncycle == k.ncycle and self.distance(k,i) % 2 == 1 :
                                return (i, j, k)
            node = node.ap
        return (0, 0, 0)

    def strongly_even_cycles_transposition(self) :
        # direction
        # 0 : backward
        # 1 : foreward
        def find_substitute(through, until, not_in_cycle, direction) :
            def next_node(node, direction) :
                if direction :
                    return node.ab
                else :
                    return node.ap
            node = next_node(through, direction)

            while node and node.index != until :
                if  node.index != 0 and node.ncycle != not_in_cycle and node.ccycle % 2 == 0 :
                    return node
                else :
                    node = next_node(node, direction)
            return 0


        i = self.end_index
        while i.index != 0 :
            if i.ccycle > 2 and i.tcycle == 0 and i.ccycle % 2 == 0:
                array_cycle = self.find_shuffling_edges(i)
                for cend in array_cycle.keys() :
                    size = len(array_cycle[cend])
                    outer_count = size - 1
                    (x,y) = (0,0)
                    while outer_count >= 0 :
                        (x,y) = (0,0)
                        if outer_count == size - 1 :
                            y = array_cycle[cend][outer_count]
                            if y.index != y.cbegin.index :
                                x = y.ap.ac
                            else :
                                outer_count = outer_count - 1

                        if outer_count != size - 1 :
                            x = array_cycle[cend][outer_count+1]
                            y = array_cycle[cend][outer_count+0]

                        if x.index != y.ap.ac.index :
                            x = y.ap.ac

                        node = y.ap
                        inner = 0
                        while not inner and node.index != x.index :
                            if node.ncycle == cend.ncycle :
                                inner = node
                            node = node.ap

                        (through, until,direction) = (0,0,0)
                        # Setting the through edge from right and left
                        (through_right, through_left) = (0,0)
                        (until_left, until_right) = (0, self.end_index.index+1)

                        if inner.index == inner.cend.index :
                            through_right = self.end_index
                            until_left = inner.cbegin.index
                            if y.index == y.cend.index :
                                until_left = max(until_left, y.cbegin.index)
                        elif y.index == y.cend.index :
                            through_right = self.end_index
                            until_left = y.cbegin.index
                        elif y.rac.ab.index > inner.rac.ab.index :
                            through_right = y.rac.ab
                        else :
                            through_right = inner.rac.ab

                        if inner.index == inner.cbegin.index :
                            through_left = self.begin_index
                            until_right = inner.cend.index
                            if x.index == x.cbegin.index :
                                until_right = min(until_right, x.cend.index)
                        elif x.index == x.cbegin.index :
                            through_left = self.begin_index
                            until_right = x.cend.index
                        elif x.ap.ac.index < inner.ap.ac.index :
                            through_left = x.ap.ac
                        else :
                            through_left = inner.ap.ac

                        z = find_substitute(through_left, until_left, x.ncycle, 0)
                        if z :
                            return (z,x,y)
                        else :
                            z = find_substitute(through_right, until_right,
                                                    x.ncycle, 1)
                            if z :
                                return (z,x,y)
                        outer_count = outer_count - 1

            i = i.ap
        return 0,0,0

    def even_cycles_transposition(self) :
        cycles = []
        self.clean_visit()

        node = self.end_index
        while node :
            if not node.tcycle and node.ccycle > 2 and not node.cend.visit :
                node.visit = 1
                size = len(cycles)
                if size == 0 :
                    cycles.append(node)
                elif node.cbegin.index < cycles[-1].cbegin.index :
                    if node.ccycle % 2 == 1 or cycles[-1].ccycle % 2 == 0 :
                        cycles.append(node)
                    else :
                        count = size - 1
                        while count >= 0 and cycles[count].ccycle % 2 == 1 :
                            count = count - 1
                        cycles.insert(count, node)
                    cycles.append(node)
                else :
                    count = size - 1
                    while count >= 0 and node.cbegin.index > cycles[count].cbegin.index :
                        count = count - 1
                    cycles.insert(count, node)
            node = node.ap

        for cycle in cycles :
            node = cycle.cbegin
            while node.index != cycle.cend.index :
                #(start, until) = 1, self.end_index.index
                (start,until) = (0,0)
                if node.index == node.cbegin.index :
                    start = 1
                    until = node.cend.index - 1
                else :
                    start = cycle.cbegin.index
                    until = self.end_index.index


                through = node.rac.ab
                while through.index != cycle.cbegin.index :
                    if through.index < until :
                        (i,j,k) = self.moving_even_cycles_transposition([node],
                                                                        start, through.index, until)
                        if i and j and k :
                            return (i,j,k)
                    through = through.rac.ab
                node = node.rac.ab
        return (0,0,0)

#     # Cycle must be long
    def no_shuffling_transposition(self, cycle) :
        (y, x) = self.find_interleaving_pair(cycle.cbegin, cycle.cend)
        if not (y and x) :
            return (0,0,0)
        s = cycle.cend.ap.ac

        if y.index > s.index :
            (u,v) = self.find_interleaving_pair(cycle.cbegin, s)
            if not (u and v) :
                return (0,0,0)
            if v.index < s.index :
                return (y, x, v)
            elif v.index < y.index :
                return (y, x, u)
            elif v.index < cycle.cend.index :
                return (u, v, x)
            else :
                return (y, x, u)
        elif x.index < s.index :
            (u,v) = self.find_interleaving_pair(s, cycle.cend)
            if not (u and v) :
                return (0, 0, 0)
            if u.index > x.index :
                return (y, x, v)
            else :
                return (u, v, y)
        elif x.index < cycle.cend.index :
            (u,v) = self.find_interleaving_pair(cycle.cbegin,s)
            if not (u and v) :
                return (0, 0, 0)
            if v.index < s.index :
                return (u, v, x)
            else :
                return (u, v, y)
        else :
            (u,v) = self.find_interleaving_pair(s, cycle.cend)
            if not (u and v) :
                return (0, 0, 0)
            return (u, v, x)
        return (0,0,0)

    def two_cycles_transposition(self) :
        node = self.end_index
        C = 0
        while node :
            if node.ccycle == 2 :
                if not C :
                    C = node
                elif node.ncycle == C.ncycle :
                    C = 0
                else :
                    return (node.cbegin, node.cend, C.cend)
            node = node.ap
        return (0, 0, 0)


class cycle_configuration_graph(cycle_graph) :
    def __init__(self, cycles, shift = 0, mirror = 0) :
        def is_oriented(cycle) :
            previous = cycle[0]
            for count in range(1,len(cycle)) :
                if previous < cycle[count] :
                    return 1
                previous = cycle[count]
            return 0

        self.n = 0
        for cycle in cycles :
            self.n = self.n + len(cycle)

        n = self.n
        self.num_cycles = len(cycles)

        # Creating ap and ab
        node_list_index = []
        node_list_index = [cycle_graph_node(i,-1) for i in range(n+1)]
        self.begin_index = node_list_index[0]
        self.end_index = node_list_index[-1]

        for i in range(n) :
            node_list_index[i].ab       = node_list_index[(i+1)]
            node_list_index[(i+1)].ap = node_list_index[i]

        # Creating ac and rac
        for i in range(len(cycles)) :
            cycle = cycles[i]

            ccycle = len(cycle)
            tcycle = is_oriented(cycle)
            ncycle = i+1
            cbegin = node_list_index[cycle[-1]]
            cend = node_list_index[cycle[0]]

            for j in range(ccycle) :
                node_list_index[cycle[j]].ccycle = ccycle
                node_list_index[cycle[j]].tcycle = tcycle
                node_list_index[cycle[j]].ncycle = ncycle
                node_list_index[cycle[j]].cbegin = cbegin
                node_list_index[cycle[j]].cend = cend

                node_list_index[cycle[j]].rac                    = node_list_index[(cycle[(j-1)%ccycle]-1)]
                node_list_index[(cycle[(j-1)%ccycle]-1)].ac = node_list_index[cycle[j]]

    def get_cycles1(self) :
        self.clean_visit()
        node = self.begin_index.ab
        cycles = []
        while node :
            cycle = []
            local_node = node
            while not local_node.visit :
                cycle.append(local_node.index)
                local_node.visit = 1
                local_node =  local_node.ap.ac
            if len(cycle) :
                cycles.append(cycle)
            node = node.ab
        return cycles


    def is_ordered(self) :
        node = self.begin_index.ab
        while node :
            if node.ap.ac.index != node.index :
                return False
            node = node.ab
        return True

class cycle_graph_node :

    #value  : stores pi_i
    #index  : stores the black edge i, 0 <= i <= n+1
    #ap     : points to the record that stores pi_{i-1}, 1 <= i <= n+1
    #ab     : points to the record that stores pi_{i+1}, 0 <= i <= n
    #ac     : points to the record that stores i + 1,    0 <= i <= n
    #visit  : indicates if the record has been visited
    #ccycle : stores the length of the cycle to which pi_i belongs
    #tcycle : stores 1 if the cycle is oriented or 0 if it is non-oriented
    #ncycle : is a unique identifier for the cycle
    #pcycle : stores the cycle position of the element in the canonical representation
    #cbegin : stores the black edge i_1 in the canonical representation
    #cend   : stores the black edge i_k in the canonical representation
    def __init__(self, index, value) :
        self.index, self.value = index, value
        self.ap, self.ab, self.ac, self.rac = 0,0,0,0
        self.visit = 0
        self.ccycle, self.tcycle, self.ncycle = 0,0,0
        self.cbegin, self.cend = 0,0

    def set_pointers(self, ap = 0, ab = 0, ac = 0) :
        if ap :
            self.ap = ap
        if ab :
            self.ab = ab
        if ac :
            self.ac = ac


    def __str__(self) :
        str =  "pi_{%i} = %i|{ccycle=%i, tcycle=%i, ncycle=%i}" % (
            self.index, self.value, self.ccycle, self.tcycle, self.ncycle)

        if self.cbegin :
            str = str + ", cbegin=%i" % self.cbegin.index

        if self.cend :
            str = str + ", cend=%i" % self.cend.index

        if self.ab :
            str = str + ", ab=%i" % self.ab.index

        if self.ap :
            str = str + ", ap=%i" % self.ap.index

        if self.ac :
            str = str + ", ac=%i" % self.ac.index

        if self.rac :
            str = str + ", rac=%i" % self.rac.index

        str = str + "}"

        return str

if __name__ == "__main__" :
    dias = dias2010(sys.argv[1])
    dias.sort()
