/***********************************************************
 * Created: Wed 02 Aug 2017 02:20:22 PM BRST
 *
 * Author: Alexsandro Alexandrino, a.o.alexsandro@gmail.com
 *
 ***********************************************************/


#ifndef __WEIGHTED_REVERSAL_GREEDY_H
#define __WEIGHTED_REVERSAL_GREEDY_H

#include "../util.h"
#include "../permutations.h"

int first_strip_end(permutation_t *p);
int find_strip_containing(permutation_t *p, int value, int asc);
void alg_2R_g(permutation_t *p, int verbose, info_t* info);

#endif /* __WEIGHTED_REVERSAL_GREEDY_H */
