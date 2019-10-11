#!/usr/bin/python
import sys

def positions(permutation):
    n = len(permutation) - 1
    p =  [0 for i in range(n + 1)]
    for i in range(n+1):
        p[permutation[i]] = i
    return p

def transposition(permutation, i, j, k) :
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
        new.append(permutation[j-x+i])
    for x in range(j+1,n):
        new.append(permutation[x])
    return new

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


def sort(param_pi) :
    distance = 0
    sequence = []
    pi = param_pi
    n = len(pi) - 2
    while pi != range(len(pi)) :
        position = positions(pi)
        move     = None

        ## Find where finishes the first strip
        i = 0
        while pi[i+1] == pi[i] + 1 :
            i = i + 1

        succ = pi[i]+1

        pos_succ = position[succ]
        if pi[pos_succ - 1] == succ + 1 :
            move = [i+1, pos_succ]
            pi = reversal(pi, i+1, pos_succ)
        else :

            ## We have to guarantee that we will never break the last
            ## strip
            k = len(pi)-1
            while pi[k-1] == pi[k] - 1 :
                k = k - 1

            move = [i+1, pos_succ, k]
            pi = transposition(pi, i+1, pos_succ, k)

        sequence.append(move)

    res = open(sys.argv[2], "a")
    sor = open(sys.argv[3], "a")
    print >> sor, ("%s" % sequence)
    #print >> res, ("%d" % len(sequence))
    weight = 0
    for t in sequence:
        if len(t) == 3:
            weight += fw_t(t[0],t[1],t[2],n)
        else:
            weight += fw_r(t[0],t[1],n)
    print >> res, ("%d" % weight)
    #return sequence

if __name__ == '__main__':
    array = eval("[0,%s]" % sys.argv[1])
    array.append(len(array))
    sort(array)
