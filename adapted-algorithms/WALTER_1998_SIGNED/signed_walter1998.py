#!/usr/bin/python

import commands
import sys
import signed_cycle_decomposition

def fw_r(i, j, size):
  if(i == 1 and j == size):
    return 0
  elif(i == 1 or j == size):
    return 1
  else:
    return 2

def fw_t(i, j, k, size):
    if (i == 1 and k == size+1):
        return 1;
    elif (i == 1 or k == size+1):
        return 2;
    else:
        return 3;

def transposition(permutation,i,j,k):
  n = len(permutation)
  new = []
  for x in range(0,i):
    new.append(permutation[x])
  for x in range(j,k):
    new.append(permutation[x])
  for x in range(i,j):
    new.append(permutation[x])
  for x in range(k,n):
    new.append(permutation[x])
  return new

def reversal(permutation,i,j):
  n = len(permutation)
  new = []
  for x in range(0,i):
    new.append(permutation[x])
  for x in range(i,j+1):
    new.append(-permutation[j-x+i])
  for x in range(j+1,n):
    new.append(permutation[x])
  return new

def get_cycles(str_permutation) :
    return signed_cycle_decomposition.cycle_decompositon(str_permutation)

def get_rightmost_element(cycle, position) :
    max_position = 0
    for i in range(len(cycle)) :
        if position[cycle[i]] > position[cycle[max_position]] :
            max_position = i
    return max_position


def one_reversal(cycle, position) :
    index = get_rightmost_element(cycle, position)

    first_black = []
    traversal   = 0

    if index % 2 == 0 :
        first_black = [ index, (index-1) % len(cycle) ]
        traversal   = -1
    else :
        first_black = [ index, (index+1) % len(cycle) ]
        traversal   = + 1

    black = first_black
    while True :
        next_black = [ (black[0]+2*traversal)%len(cycle), (black[1]+2*traversal)%len(cycle)]
        if first_black == next_black :
            break

        if not ( position[cycle[black[0]]]       - position[cycle[black[1]]] ==
                 position[cycle[next_black [0]]] - position[cycle[next_black [1]]]     ):

            indices  = [i%len(cycle) for i in  range(black[1],
                                                     len(cycle)*traversal+black[1],
                                                     traversal)]

            new_cycles = [[]]
            for index in indices :
                new_cycles[-1].append(cycle[index])
                if index in (black[0], next_black[0]) :
                    new_cycles.append([])


            #print(cycle)
            #print("Black = ", "%i,%i" % (position[cycle[black[0]]], position[cycle[black[1]]]))
            #print("Next-Black = ", "%i,%i" % (position[cycle[next_black[0]]], position[cycle[next_black[1]]]))
            #print(position)

            max_black = max(position[cycle[black[0]]],        position[cycle[black[1]]])
            min_black = min(position[cycle[black[0]]],        position[cycle[black[1]]])
            max_next  = max(position[cycle[next_black [0]]],  position[cycle[next_black [1]]])
            min_next  = min(position[cycle[next_black [0]]],  position[cycle[next_black [1]]])

            if max_black < max_next :
                return ([max_black,
                        min_next],
                        new_cycles[:-1])
            else :
                return ([max_next,
                         min_black],
                        new_cycles[:-1])

        black = next_black
    # else :
    #     first_black = [ index, (index+1) % len(cycle) ]
    #     black = first_black
    #     while True :
    #         next_black = [ (black[0]+2)%len(cycle), (black[1]+2)%len(cycle)]
    #         if first_black == next_black :
    #             break
    #         if not ( position[cycle[black[0]]]       - position[cycle[black[1]]] ==
    #                  position[cycle[next_black [0]]] - position[cycle[next_black [1]]]     ):
    #             if position[cycle[black[0]]] < position[cycle[next_black [0]]] :
    #                 return [max(position[cycle[black[0]]],        position[cycle[black[1]]]),
    #                         min(position[cycle[next_black [0]]],  position[cycle[next_black [1]]])]
    #             else :
    #                 return [max(position[cycle[next_black [0]]],  position[cycle[next_black [1]]]),
    #                         min(position[cycle[black[0]]],        position[cycle[black[1]]])]

    #         black = next_black
    return ([0, 0], [])

def two_transposition(cycle, position) :
    index = get_rightmost_element(cycle, position)

    first_black = []
    traversal   = 0

    if index % 2 == 0 :
        first_black = [ index, (index-1) % len(cycle) ]
        traversal   = -1
    else :
        first_black = [ index, (index+1) % len(cycle) ]
        traversal   = + 1

    black = first_black
    while True :
        next_black = [ (black[0]+2*traversal)%len(cycle), (black[1]+2*traversal)%len(cycle)]
        if first_black == next_black :
            break
        if position[cycle[black[0]]] < position[cycle[next_black[0]]] :


            ## Check if it is oriented or semi-oriented triple
            if ( position[cycle[black[0]]]       - position[cycle[black[1]]]       ==
                 position[cycle[next_black [0]]] - position[cycle[next_black [1]]] ==
                 position[cycle[first_black[0]]] - position[cycle[first_black[1]]] ) :

                indices  = [i%len(cycle) for i in  range(first_black[1],
                                                         len(cycle)*traversal+first_black[1],
                                                         traversal)]
                new_cycles = [[]]
                for index in indices :
                    new_cycles[-1].append(cycle[index])
                    if index in (black[0], next_black[0], first_black[0]) :
                        new_cycles.append([])

                return ([ max(position[cycle[black[0]]],      position[cycle[black[1]]]),
                          max(position[cycle[next_black[0]]], position[cycle[next_black[1]]]),
                          position[cycle[first_black[0]]]], new_cycles[:-1])
            else :
                return ([0,0,0], [])
        black = next_black
    return ([0,0,0], [])

def interleaving_edges(i, j, cycles) :
    for count in range(len(cycles)) :
        cycle = cycles[count]
        if len(cycle) > 2 :
            #print(cycle, i, j)
            index = get_rightmost_element(cycle, position)

            #print("rightmost", index)

            first_black = []
            traversal   = 0

            if index % 2 == 0 :
                first_black = [ index, (index-1) % len(cycle) ]
                traversal   = -1
            else :
                first_black = [ index, (index+1) % len(cycle) ]
                traversal   = + 1

            black = first_black
            #print("first_black = ", "[%s-%s]" % (cycle[black[0]], cycle[black[1]]))
            while True :

                next_black = [ (black[0]+2*traversal)%len(cycle), (black[1]+2*traversal)%len(cycle)]
                if first_black == next_black :
                    break
                #print("next_black = ", "[%s-%s]" % (cycle[next_black[0]], cycle[next_black[0]]))

                #print("i,j = ", "%i,%i" % (i,j))
                #print("edges=", "%i,%i" % (position[cycle[next_black[0]]], position[cycle[black[1]]]))
                if (i < position[cycle[next_black[0]]] < j < position[cycle[black[0]]]) :
                    return count, next_black, traversal
                elif (position[cycle[next_black[0]]] < i < position[cycle[black[0]]] < j) :
                    return count, black, traversal
                black = next_black

    print("Error: ", sys.argv[1] )


def zero_transposition(cycle_1, cycles, position) :
    index = get_rightmost_element(cycle_1, position)

    #print(cycle_1)

    first_black_1  = []
    second_black_1 = []
    traversal_1      = 0

    if index % 2 == 0 :
        first_black_1  = [ index, (index-1) % len(cycle_1) ]
        second_black_1 = [ (first_black_1[0]-2)%len(cycle_1), (first_black_1[1]-2)%len(cycle_1)]
        traversal_1     = -1
    else :
        first_black_1  = [ index, (index+1) % len(cycle_1) ]
        second_black_1 = [ (first_black_1[0]+2)%len(cycle_1), (first_black_1[1]+2)%len(cycle_1)]
        traversal_1      = +1

    cycle_2_index, black_2, traversal_2 = interleaving_edges(position[cycle_1[second_black_1[0]]],
                                                             position[cycle_1[first_black_1[0]]],
                                                             cycles)
    cycle_2 = cycles[cycle_2_index]

    new_cycle1 = [cycle_1[first_black_1[1]], cycle_1[second_black_1[0]]]

    new_cycle2 = []
    ## Primeiro eu vou adicionar o ciclo interno
    indices_2  = [i%len(cycle_2) for i in  range(black_2[1],
                                                 len(cycle_2)*traversal_2+black_2[1],
                                                 traversal_2)]
    for index in indices_2 :
        new_cycle2.append(cycle_2[index])
        if index == black_2[0] :
            break

    ## Agora eu vou adicionar o ciclo que veio como parametro
    indices_1  = [i%len(cycle_1) for i in  range(second_black_1[1],
                                                 len(cycle_1)*traversal_1+second_black_1[1],
                                                 traversal_1)]
    for index in indices_1 :
        new_cycle2.append(cycle_1[index])
        if index == first_black_1[0] :
            break

    return ([position[cycle_1[second_black_1[0]]],
             position[cycle_2[black_2[0]]],
             position[cycle_1[first_black_1[0]]]], [new_cycle1, new_cycle2], cycle_2_index)


def get_position(permutation) :
    position    = [-1 for i in range(0, n+2)]
    for i in range(0, n+2) :
        position[abs(permutation[i])] = i
    return position

if __name__ == "__main__" :
    permutation = []
    identity = []
    sequence = []
    distance = 0
    position = 0
    n = 0
    cycles = []
    str_permutation = ""

    file = open(sys.argv[1], 'r')
    max_range = int(sys.argv[4])
    for i in range(max_range):
        str_permutation = file.readline()
        cycles      = get_cycles(str_permutation)
        #print(cycles)
        permutation = eval("[%s]" % str_permutation)
        n = len(permutation)
        permutation = [0] + permutation + [n+1]
        identity    = range(len(permutation))

        position    = get_position(permutation)

        distance = 0
        sequence = []
        while permutation != identity :

            operation_performed = False

            if not operation_performed :
                ## Check if g(\pi) has semi_oriented_cycles
                for cycle_index in range(len(cycles)) :
                    cycle = cycles[cycle_index]
                    if len(cycle) > 2 :
                        [i,j], new_cycles = one_reversal(cycle, position)
                        if [i,j] != [0,0] :
                            # print("1-Reversal", permutation, cycle, new_cycles, "  > ", i, j )
                            permutation = reversal(permutation, i, j)
                            position    = get_position(permutation)
                            distance    = distance + 1
                            sequence.append([i,j])
                            cycles.__delitem__(cycle_index)
                            cycles = cycles + new_cycles
                            operation_performed = True
                            break


            ## Starting sort
            ## Check if g(\pi) has oriented cycles
            if not operation_performed :
                for cycle_index in range(len(cycles)) :
                    cycle = cycles[cycle_index]
                    if len(cycle) > 3 :
                        [i,j,k], new_cycles = two_transposition(cycle, position)
                        if [i,j,k] != [0,0,0] :
                            # print("2-Transposition", cycle, new_cycles)
                            permutation = transposition(permutation, i, j,k)
                            position    = get_position(permutation)
                            distance    = distance + 1
                            sequence.append([i,j,k])
                            cycles.__delitem__(cycle_index)
                            cycles = cycles + new_cycles
                            operation_performed = True
                            break


            if not operation_performed :
                ## Check if g(\pi) has non-oriented cycles
                for cycle_index in range(len(cycles)) :
                    cycle = cycles[cycle_index]
                    if len(cycle) > 2 :
                        [i,j,k], new_cycles, obsolete_cycle_index = zero_transposition(cycle, cycles, position)
                        # print("0-Transposition", permutation , [cycle, cycles[obsolete_cycle_index]], new_cycles)
                        permutation = transposition(permutation, i, j,k)
                        position    = get_position(permutation)
                        distance    = distance + 1
                        sequence.append([i,j,k])
                        cycles.__delitem__(cycle_index)
                        if cycle_index < obsolete_cycle_index :
                            obsolete_cycle_index = obsolete_cycle_index - 1
                        cycles.__delitem__(obsolete_cycle_index)
                        cycles = cycles + new_cycles
                        operation_performed = True
                        break

            if not operation_performed :
                print("Error: Something wrong Happened", sys.argv[1],permutation, cycles)
                sys.exit()


            #print(permutation, cycles)
        #print len(sequence),
        #print(sequence)

        res = open(sys.argv[2], "a")
        sor = open(sys.argv[3], "a")
        #print >> res, ("%d" % len(sequence))
        print >> sor, ("%s" % sequence)
        weight = 0
        for t in sequence:
            if len(t) == 3:
                weight += fw_t(t[0],t[1],t[2],n)
            else:
                weight += fw_r(t[0],t[1],n)
        print >> res, ("%d" % weight)
