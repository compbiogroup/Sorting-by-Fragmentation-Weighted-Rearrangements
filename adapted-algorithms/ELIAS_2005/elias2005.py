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

 # If you use this softwore anytime in your work, please cite the
 # following papers:
 # 
 # DIAS, U. ; DIAS, Z. . Extending Bafna-Pevzner algorithm. In:
 # International Symposium on Biocomputing (ISB'2010), 2010, Calicut,
 # Kerala. Proceedings of the 1st International Symposium on
 # Biocomputing (ISB'2010). New York, NY, USA : ACM, 2010. p. 1-8.
 # 
 # DIAS, U. ; DIAS, Z. . An Improved 1.375-Approximation Algorithm for
 # the Transposition Distance Problem. In: International Conference on
 # Bioinformatics and Computational Biology (ACM-BCB'2010), 2010,
 # Niagara Falls, NY, USA. Proceeding of the 1st ACM International
 # Conference on Bioinformatics and Computational Biology
 # (ACM-BCB'2010). New York, NY, USA : ACM, 2010. p. 334-337.
 # 
 # Elias, I. ; Hartman, T. . A 1.375-Approximation Algorithm for
 # Sorting by Transpositions. IEEE/ACM Transactions on Computational
 # Biology and Bioinformatics, 3(4):369-279,2006.

import sys
import copy
import math
import re

def cost(i,j,k,n):
    if i == 1 and k == n+1:
        return 1
    elif i == 1:
        return 2
    elif k == n+1:
        return 2
    else:
        return 3

class elias2005 :
    def __init__(self, param_permutation) :
        self.input = param_permutation
        param_permutation =  param_permutation.split(",")
        self.permutation = []
        self.trace = ""
        for item in param_permutation :
            self.permutation.append(int(item))

    def is_reversal(self, permutation) :
        size = len(permutation)
        for i in range(size) :
            if int(permutation[i]) != ((size -(i + 1)) % size) + 1 :
                return False
        return True

    def sort(self) :
        distance = 0
        permutation = self.permutation
        graph = cycle_graph(permutation)
        graph.transform_into_simple_permutation()
        graph.transform_into_simple_permutation()
        graph.transform_into_simple_permutation()
        graph.transform_into_simple_permutation()
        graph.transform_into_simple_permutation()
        graph.transform_into_simple_permutation()
        graph.transform_into_simple_permutation()
        #print(graph.get_cycles(), graph.n)
        permutation_size = graph.n
        while not graph.is_ordered() :
            try :
                transpositions = self.sort_steps(graph)
                for transposition in transpositions :
                    (i,j,k) = transposition
                    #print(transposition, cost(i,j,k, permutation_size))
                    distance = distance + cost(i,j,k, permutation_size)
                    graph.transposition(i,j,k)
            except :
                print("Erro %s" % permutation.__str__())
                print("elias2005 - %s - %i - []" % (self.input, distance))
                sys.exit()

        print("%i" % (distance))

    def test(self) :
        graph = cycle_graph(self.permutation)
        graph.transform_into_simple_permutation()
        transpositions = graph.get_1_375_move()


    def sort_steps(self, graph) :

        oriented_cycle = graph.get_oriented_cycle()
        if oriented_cycle :
            transp = [oriented_cycle.ap.ac.index, 
                      oriented_cycle.ap.ac.ap.ac.index, 
                      oriented_cycle.index]
            
            transp.sort()
            return [transp]
        

        cycle1, cycle2 = graph.get_two_cycle()

        if cycle1 and cycle2 :
            transp = [cycle1.index, cycle2.index, cycle1.cend.index]
            transp.sort()
            return [transp]

        transpositions = graph.get_database_move()
        if transpositions :
           return transpositions
        

        

class cycle_graph :
    def __init__(self, permutation) :
        n = len(permutation)
        self.n = n
        self.num_cycles = 0
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
        n = self.n
        self.clean_visit()
        self.clean_orientation()

        # Theorem 5: decomposing cycles
        cycles = []
        for i in range(1,n+2) :
            local_node = node_list_index[-i]
            cycle = []
            while not local_node.visit :
                cycle.append(local_node.index)
                local_node.visit = 1
                local_node =  local_node.ap.ac
            if len(cycle) :
                cycles.append(cycle)
                
        self.num_cycles = len(cycles)
        for i in range(self.num_cycles) :
            cycle = cycles[i]
            ccycle = len(cycle)
            cend = node_list_index[cycle[0]]
            for element in cycle :
                node_list_index[element].ccycle = ccycle
                node_list_index[element].cend = cend

    def transform_into_simple_permutation(self) :
        node = self.begin_index.ab
        while node :
            if node.cend.ccycle > 3  :
                b3 = node.cend
                b1 = b3.ap.ac
                b2 = b1.ap.ac.ap
                
                #Creating a new vertex that will be inserted
                aux_index = b3.index
                if aux_index == 0 :
                    aux_index = self.n+1
                index = (float(aux_index + b3.ap.index))/2
                value = (float(b2.value + b2.ac.value))/2
                v = cycle_graph_node(index,value)

                # Inserting new vertex before the vertex b3
                v.ab = b3
                v.ap = b3.ap
                b3.ap = v
                v.ap.ab = v

                # linking v to the node that b2 is pointing
                v.ac = b2.ac
                v.ac.rac = v

                # Creating the gray edge linking b2 to v and
                # updating the value of cend
                b2.ac  = v
                v.rac  = b2

                # Updating information of the modified cycle
                inner_node = b3
                while True :
                    inner_node.ccycle = inner_node.ccycle - 2
                    inner_node.tcycle = -1
                    inner_node = inner_node.ap.ac
                    if inner_node.index == b3.index :
                        break
                  
                # Generating information for the created cycle
                b2.ab.cend = v
                b1.cend = v
                v.cend = v
                b2.ab.ccycle = 3
                b1.ccycle = 3
                v.ccycle = 3

            node = node.ab
        self.relabel_index_and_value()

    def relabel_index_and_value(self) :
        node = self.begin_index
        count = 0 
        while node :
            node.index = count
            count = count + 1
            node = node.ab

        node = self.begin_index
        count = 0
        while node :
            node.value = count
            count = count + 1
            node = node.ac
        self.n = count -2

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

    def clean_orientation(self) :
        node = self.begin_index
        while node :
            node.tcycle = -1
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
            
    def get_oriented_cycle(self) :
        node = self.begin_index.ab
        while node :
            if node.is_oriented() :
                return node.cend
            node = node.ab
        return 0

    def get_two_cycle(self) :
        node = self.begin_index
        C = 0
        while node :
            if node.ccycle == 2 :
                if C :
                    if node.cend.index != C.cend.index :
                        return C, node
                else :
                    C = node
            node = node.ab
        return 0,0

    def get_closing_open_gates_extension(self, component) :
        def get_index(node) :
            return node.index

        component_elements = list(component)
        for cycle in component :
            component_elements.append(cycle.ap.ac) 
            component_elements.append(cycle.rac.ab)
        component_elements.sort(key=get_index)
        
        if component_elements[0].cend.index == component_elements[-1].cend.index :
            node = self.begin_index.ab 
            while node.index < component_elements[0].index :
                if node.ccycle == 3 :
                    for comp_cycle in component :
                        if comp_cycle.is_intersecting(node) :
                            return node.cend
                node = node.ab
                
            node = component_elements[-1].cend.ab 
            while node : 
                if node.ccycle == 3 :
                    for comp_cycle in component :
                        if comp_cycle.is_intersecting(node) : 
                            return node.cend
                node = node.ab

        for i in range(1,len(component_elements)) :
            if component_elements[i-1].cend.index == component_elements[i].cend.index :
                node = component_elements[i-1].ab
                while node.index < component_elements[i].index :
                    if node.ccycle == 3 :
                        for comp_cycle in component :
                            if comp_cycle.is_intersecting(node) :
                                return node.cend
                    node = node.ab
        return 0


    def extend_component(self, component, components) :
        num_nodes  = len(components)
        
        #print("EXTENDING")
        close_node = self.get_closing_open_gates_extension(component)
        if close_node :
            for el in range(num_nodes) :
                if components[el].index == close_node.index :
                    #print("DELETING")
                    components.__delitem__(el)
                    break
            component.append(close_node)
            return(component, components)

        #print("NO OPEN")
        for el in range(num_nodes) :
            node = components[el]
            #print("TRYING %i" % node.index)
            for comp_cycle in component :
                if comp_cycle.is_intersecting(node) :
                    #print("INTERSECTION %i %i" % (comp_cycle.index, node.index))
                    components.__delitem__(el)
                    component.append(node)
                    return(component, components)
        return (0,0)

    def format_component(self, component) :
        def get_leftmost(cycle) :
            return cycle[0]

        node = self.begin_index.ab

        hash_component = {}
        ordered = []
        count = 1
        while node :
            for cycle in component :
                if node.cend.index == cycle.index :
                    if cycle in hash_component :
                        hash_component[cycle].insert(0,count)
                    else :
                        hash_component[cycle] = [count]
                    ordered.append(node.index)
                    count = count + 1
                    break
            node = node.ab
        
        cycles_list = list(hash_component.values())
        cycles_list.sort(key=get_leftmost,reverse=1)
        return ordered, cycles_list
        

    def get_transposition_in_database(self, database, component) :
        def cycles_to_string(cycles) : 
            cycles_str = ""
            for cycle in cycles :
                cycles_str = "%s(%i %i %i)" % (cycles_str,cycle[0],cycle[1],cycle[2])
            return cycles_str

        def string_to_transpositions(transps_string) :
            transps_string = transps_string[1:-1]
            transps_string = transps_string.split(")(")
            transpositions = []
            for transp_string in transps_string :
                transp_string = transp_string.split(",")
                transposition = []
                transposition.append((int)(transp_string[0]))
                transposition.append((int)(transp_string[1]))
                transposition.append((int)(transp_string[2]))
                transpositions.append(transposition)
            return transpositions

        def search_database(database, key) :
            file = open("elias2005.db.%s" % database, 'r')
            #print(file)
            for line in file :
                match = re.match("(.*):(.*)", line)
                if match :
                    if match.group(1) == key :
                        return string_to_transpositions(match.group(2).rstrip())
            return 0   

        def get_delta_array(vector) :
            delta_array = []
            for i in range(1,len(vector)) :
                delta_array.append(vector[i] - vector[i-1])
            return delta_array

        def set_delta_array(start_point, delta_vector) :
            vector = [start_point]
            for i in range(len(delta_vector)) :
                vector.append(vector[i] + delta_vector[i])
            return vector

        (indices, cycles) = self.format_component(component)
        delta_indices = get_delta_array(indices)

        key = cycles_to_string(cycles)
        database_trans = search_database(database, key)
        if database_trans : 
            transpositions = []
            for old_trans in database_trans :
                transposition = []
                i = old_trans[0]
                j = old_trans[1]
                k = old_trans[2]
                transposition.append(indices[i-1])
                transposition.append(indices[j-1])
                transposition.append(indices[k-1])
                transpositions.append(transposition)
                
                delta_indices = (delta_indices[0:i-1]   + 
                                 delta_indices[j-1:k-1] + 
                                 delta_indices[i-1:j-1] +
                                 delta_indices[k-1:len(delta_indices)])
                indices = set_delta_array(indices[0], delta_indices)

#                 # Adjunting indices
#                 delta_b1 =  (indices[old_trans[1]-1]-indices[old_trans[0]-1])-(old_trans[1]-old_trans[0])
#                 delta_b2 =  (indices[old_trans[2]-1]-indices[old_trans[1]-1])-(old_trans[2]-old_trans[1])
#                 for count_indice in range(indices) :
#                     if   count_indice + 1 <= indices[old_trans[0]-1] :
#                         pass
#                     elif count_indice + 1 >= indices[old_trans[2]-1] :
#                         pass
#                     elif count_indice + 1 >= indices[old_trans[1]-1] :
#                         indices[count_indice] = indices[count_indice] + delta_b2 - delta_b1
#                     else :
#                         indices[count_indice] = indices[count_indice] - delta_b2 + delta_b1

            return transpositions
        return 0

  
    def get_database_move(self) :
        # Main Function

        # Split the cycles in components
        aux_hash = {}
        components = []
        node = self.begin_index.ab
        while node : 
            if node.ccycle == 3 and not (node.cend in aux_hash) :
                aux_hash[node.cend] = 1
                components.insert(0,node.cend)
            node = node.ab

        # Array used to save the components that dont allow 1_375 moves
        # May be used to combine different components
        data = []

        #components = list(aux_hash.keys())

        while len(components) > 0 :
            component = [components[0]]
            components.__delitem__(0)
            #print("FIRST = %i" % component[0].index)

            # This will not fail by definition
            (component,components) = self.extend_component(component, components)
            
            (new_component, new_components) = self.extend_component(component, components)
            while new_component :
                (component, components) = (new_component, new_components)
                database = "%i" % (len(component)*3)
                transpositions = self.get_transposition_in_database(database, component)
                if transpositions:
                    return transpositions
                (new_component, new_components) = self.extend_component(component, components)
                
            data.append(component)
            
        # There is no component allowing a 1_375 move, but
        # but maybe a combination of components may be a
        # a good approach
        if len(data) > 1 :
            size = 0
            combination = []
            for component in data : 
                combination = combination + component
                if len(combination) > 7 :
                    database = "comb"

                    transpositions = self.get_transposition_in_database(database, combination)
                    if transpositions :
                        return transpositions

        # There is no component allowing a 1_375 and neither
        # a 1_375 combination is available
        # In this case we apply a 1_5 move
        database = "bad"
        transpositions = self.get_transposition_in_database(database, data[0])
        if transpositions :
            return transpositions

    def get_edges(self) :
        node = self.begin_index
        edges = []
        while node.ac : 
            edges.append([node.index, node.ac.index])
            node = node.ab
        return edges

    def get_cycles(self) :
        self.clean_visit()
        node = self.begin_index.ab 
        cycles = []
        while node :
            cycle = []
            local_node = node.cend
            while not local_node.visit :
                cycle.append(local_node.index)
                local_node.visit = 1
                local_node =  local_node.ap.ac
            if len(cycle) :
                cycles.append(cycle)
            node = node.ab
        return cycles

    def lower_bound(self) :
        cycles = self.get_cycles()
        num_odd = 0
        for cycle in cycles :
            if len(cycle) % 2 == 1:
                num_odd = num_odd + 1

        return math.ceil((self.n - num_odd)/2)

    def __str__(self) :
        str = ""
        node = self.begin_index
        while node :
            #str = str + "%s\n" % node.__str__()
            str = str + "%s," % node.value
            #str = str + "%s = %s, tcycle = %s \n" % (node.index, node.value, node.tcycle)
            node = node.ab
        return str



############################################################################
############ Same as Cycle_Graph, but starts with cycles ###################
############################################################################
############ Do not need to represent a real permutation ###################
############################################################################
########### The transposition and other methos still work ##################
############################################################################

class cycle_graph_by_cycles(cycle_graph) :
    def __init__(self, cycles) :
        self.n = 0
        for cycle in cycles :
            self.n = self.n + len(cycle)
        # self.n = self.n - 1
        
        n = self.n
        self.num_cycles = len(cycles)
          
        # Creating ap and ab
        node_list_index = []
        node_list_index = [cycle_graph_node(i,-1) for i in range(n+1)]
        self.begin_index = node_list_index[0]

        for i in range(n) :
            node_list_index[i].ab       = node_list_index[(i+1)]
            node_list_index[(i+1)].ap = node_list_index[i]

        # Creating ac and rac
        for cycle in cycles :
            size = len(cycle)
            cend = node_list_index[cycle[0]]
            for i in range(size) :
                node_list_index[cycle[i]].cend = cend
                node_list_index[cycle[i]].rac                    = node_list_index[(cycle[(i-1)%size]-1)]
                node_list_index[(cycle[(i-1)%size]-1)].ac = node_list_index[cycle[i]]

        # Labeling the nodes
        local_node = self.begin_index
        local_node.value = 0
        while local_node.ac :
            next_node = local_node.ac
            next_node.value = local_node.value + 1
            local_node = next_node


    def is_ordered(self) :
        node = self.begin_index.ab 
        while node :
            if node.ap.ac.index != node :
                return False
            node = node.ab
        return True

    def __str__(self) :
        cycles = self.get_cycles()
        str = ""
        for cycle in cycles :
            str = "%s%s" % (cycle, str)
        return str

    def get_permutation(self) :
        str = ""
        node = self.begin_index.ab
        while node.ab :
            #str = str + "%s\n" % node.__str__()
            str = str + "%s," % node.value
            #str = str + "%s = %s, tcycle = %s \n" % (node.index, node.value, node.tcycle)
            node = node.ab
        return str[0:-1]        

############################################################################
############################## NEW CLASS ###################################
############################################################################
############ Do not need to represent a real permutation ###################
############################################################################

class cycle_configuration_graph(cycle_graph) :
    def __init__(self, cycles, shift = 0, mirror = 0) :
        self.n = 0
        for cycle in cycles :
            self.n = self.n + len(cycle)

        n = self.n
        self.num_cycles = len(cycles)
          
        # Creating ap and ab
        node_list_index = []
        node_list_index = [cycle_graph_node(i,-1) for i in range(n+1)]
        self.begin_index = node_list_index[0]

        for i in range(n) :
            node_list_index[i].ab       = node_list_index[(i+1)]
            node_list_index[(i+1)].ap = node_list_index[i]

        # Creating ac and rac
        for cycle in cycles :
            size = len(cycle)
            cend = node_list_index[cycle[0]]
            for i in range(size) :
                node_list_index[cycle[i]].cend = cend
                node_list_index[cycle[i]].rac                    = node_list_index[(cycle[(i-1)%size]-1)]
                node_list_index[(cycle[(i-1)%size]-1)].ac = node_list_index[cycle[i]]

        node = self.begin_index.ab
        count = 1
        while node :
            node.value = (count + shift) % n
            if not node.value :
                node.value = n
            node = node.ab
            count = count + 1

        if mirror % 2 : 
            node = self.begin_index.ab
            while node :
                node.value = (n - node.value) % n
                if not node.value :
                    node.value = n
                node = node.ab

    def get_value_by_index(self, index) :
        values = []
        n = self.n
        node = self.begin_index.ab
        while node :
            local_value = node.value

            if (node.index == index[0] or
                node.index == index[1] or
                node.index == index[2]) :
                values.append(local_value)
            node = node.ab
        return values

    def get_index_by_value(self, values) :
        index = []
        n = self.n
        node = self.begin_index.ab
        while node :
            local_index = node.index
            if not local_index :
                local_index = n
            if (node.value == values[0] or
                node.value == values[1] or
                node.value == values[2]) :
                index.append(local_index)
            node = node.ab
        return index


    def decompose_cycles(self, array) :
        pass

#####################################################################
################## REPRESENTS A NODE OF A GRAPH #####################
#####################################################################

class cycle_graph_node :
    #value  : stores pi_i
    #index  : stores the black edge i, 0 <= i <= n+1
    #ap     : points to the record that stores pi_{i-1}, 1 <= i <= n+1
    #ab     : points to the record that stores pi_{i+1}, 0 <= i <= n
    #ac     : points to the record that stores i + 1,    0 <= i <= n
    #rac    : reverse of the ac
    #visit  : indicates if the record has been visited
    #ccycle : stores the length of the cycle to which pi_i belongs
    #tcycle : stores 1 if the cycle is oriented or 0 if it is non-oriented or
    #           -1 if this information is still not available
    #cend   : stores the black edge i_k in the canonical representation
    def __init__(self, index, value) :
        self.index, self.value = index, value
        self.ap, self.ab, self.ac = 0,0,0
        self.visit = 0
        self.ccycle, self.tcycle = 0,-1
        self.cend = 0

    def set_pointers(self, ap = 0, ab = 0, ac = 0) :
        if ap :
            self.ap = ap
        if ab :
            self.ab = ab
        if ac :
            self.ac = ac
    
    def is_oriented(self) :
        if self.cend.tcycle == -1 :
            previous = self.cend
            while True :
                node = previous.ap.ac
                if previous.index < node.index :
                    self.tcycle = 1
                    return 1
                previous = node
                if previous.ap.ac.index == self.cend.index :
                    break
            self.tcycle = 0
            return 0
        else :
            return self.cend.tcycle

    def is_intersecting(self, another_cycle) :
        cycle1 = self.cend
        cycle2 = another_cycle.cend

        if (cycle1.index < cycle2.rac.ab.index) :
            return False

        if (cycle2.index < cycle1.rac.ab.index) :
            return False

        while True :
            if (cycle1.index > cycle2.index > cycle2.rac.ab.index > cycle1.ap.ac.index) : 
                return False
            
            cycle1 = cycle1.ap.ac
            if (cycle1.index == cycle1.cend.index) :
                break

        cycle1 = another_cycle.cend
        cycle2 = self.cend
        while True :
            if (cycle1.index > cycle2.index > cycle2.rac.ab.index > cycle1.ap.ac.index) : 
                return False
            
            cycle1 = cycle1.ap.ac
            if (cycle1.index == cycle1.cend.index) :
                break  
        return True

    def change_direction(self) :
        aux = self.ac
        self.ac = self.rac
        self.rac = aux

    def __str__(self) :
        str =  "pi_{%i} = %i|{ccycle=%i, tcycle=%i}" % (
            self.index, self.value, self.ccycle, self.tcycle)

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
    elias = elias2005(sys.argv[1])
    elias.sort()
    #elias.test()
