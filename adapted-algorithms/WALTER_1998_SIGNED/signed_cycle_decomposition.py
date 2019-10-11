#!/usr/bin/python

import sys

def cycle_decompositon(str_permutation):
    permutation = eval("[%s]" % str_permutation)

    n = len(permutation)

    permutation = [0] + permutation + [n+1]
    position    = [-1 for i in range(0, n+2)]
    #sign        = [-1 for i in range(0, n+2)]


    for i in range(1, n+2) :
        position[abs(permutation[i])] = i
    #    sign    [abs(permutation[i])] = permutation[i] / abs(permutation[i])


    ## 1 if the gray edge i,-(i+1) was never used.
    gray_available     = [1 for i in range(0, n+1)]
    #black_available    = [1 for i in range(0, n+1)]

    cycles = []


    for i in range(0, n+1) :

        ##
        if gray_available[i] :

            start     = i
            cycle = [start]

            end   = start
            positive  = True

            while True :

                ## Will be used later, it says if after walking through
                ## the black edge we are in the right or in the left
                is_vertex_left = None

                if positive :
                    ## Gray edge: we are looking for the edge ( end,-(end+1) )
                    gray_available[end] = gray_available[end] - 1
                    end = end + 1
                    cycle.append(end)

                    ## Black edge: we are at the vertex -end.
                    if permutation[position[end]] > 0 :
                        # If the sign in that position is positive, than
                        # -end is in the left (cycle graph)
                        end = abs(permutation[position[end]-1])
                        is_vertex_left = False


                    else :
                        # If the sign in that position is negative, than
                        # -end is in the right (cycle graph)
                        end = abs(permutation[position[end]+1])
                        is_vertex_left = True
                else :
                    ## Gray edge: we are looking for the edge ( -end, end-1  )
                    end = end - 1                                 ##  Note we swapped
                    gray_available[end] = gray_available[end] - 1 ##  these lines
                    cycle.append(end)


                    ## Black edge: we are at the vertex +end.
                    if permutation[position[end]] > 0 :
                        # If the sign in that position is positive, than
                        # +end is in the right (cycle graph)
    #                    print("")
    #                    print(cycle)
    #                    print(end)
    #                    print(position[end])
                        end = abs(permutation[position[end]+1])
                        is_vertex_left = True
                    else :
                        # If the sign in that position is negative, than
                        # +end is in the left (cycle graph)
                        end = abs(permutation[position[end]-1])
                        is_vertex_left = False

                if end == start :
                    break
                else :
                    cycle.append(end)

                    # print(cycle, is_vertex_left, permutation[position[end]])

                    if is_vertex_left :
                        if permutation[position[end]] < 0 :
                            positive = True
                        else :
                            positive = False
                    else :
                        if permutation[position[end]] < 0 :
                            positive = False
                        else :
                            positive = True
            cycles.append(cycle)

    return cycles
