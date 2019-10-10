/***********************************************************
 * Created: Wed 02 Aug 2017 02:20:22 PM BRST
 *
 * Author: Alexsandro Alexandrino, a.o.alexsandro@gmail.com
 *
 ***********************************************************/


#ifndef __WEIGHTED_SIGNED_REVERSAL_GREEDY_H
#define __WEIGHTED_SIGNED_REVERSAL_GREEDY_H

#include "../util.h"
#include "../permutations.h"

int sr_first_strip_end(permutation_t *p);
int sr_find_strip_containing(permutation_t *p, int value, int asc);
void alg_2SR_g(permutation_t *p, int verbose, info_t* info);

#endif /* __WEIGHTED_SIGNED_REVERSAL_GREEDY_H */
