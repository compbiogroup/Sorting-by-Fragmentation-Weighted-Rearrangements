/***********************************************************
 * Created: Wed 06 Aug 2017 02:00:22 PM BRST
 *
 * Author: Alexsandro Alexandrino, a.o.alexsandro@gmail.com
 *
 ***********************************************************/

#include <stdio.h>
#include <stdlib.h>
#include "../util.h"
#include "../permutations.h"
#include "../rearrangements.h"
#include "../breakpoints.h"
#include "wsr.h"

void alg_2SR(permutation_t *p, int verbose, info_t* info) {/*{{{*/
    int i, j, next_strip;
    char pos;

    next_strip = p->size;

    j = abs(p->inv_pi[next_strip]);

    if(j != p->size){ //largest strip is not in the right position

      //gets strip's position
      i = j;

      if(p->pi[j] > 0){
        pos = 1;
      }else{
        pos = 0;
      }

      while(i > 1 && p->pi[i] == p->pi[i-1] + 1){
        i--;
      }

      while(j < p->size && p->pi[j+1] == p->pi[j] + 1){
        j++;
      }

      if(pos){
        //puts largest strip at the beginning of the permutation
        op_prefix_reversal(p, j);
        print_verbose(p, verbose, 'r', 1, j, 0);
        info->nmoves++;
        info->weight += fw_r(1, j, p->size);

        //inverts the permutation
        op_prefix_reversal(p, p->size);
        print_verbose(p, verbose, 'r', 1, p->size, 0);
        info->nmoves++;
        info->weight += fw_r(1, p->size, p->size);

      }else{
        //puts largest strip in the right position
        op_suffix_reversal(p, i);
        print_verbose(p, verbose, 'r', i, p->size , 0);
        info->nmoves++;
        info->weight += fw_r(i, p->size, p->size);
      }

    }

    while (!is_identity(p)) {

        j = abs(p->inv_pi[next_strip]);

        i = j;
        if(p->pi[j] > 0){
          pos = 1;
        }else{
          pos = 0;
        }

        while(i > 1 && p->pi[i] == p->pi[i-1] + 1){
          i--;
        }

        while(j < p->size && p->pi[j+1] == p->pi[j] + 1){
          j++;
        }

        if(i == p->pi[i] && j == p->pi[j]){
          //updates value of the next (out of place) strip
          next_strip = i-1; // \pi_i is in the right position
        }else{
          if(pos){

            op_prefix_reversal(p, j);
            print_verbose(p, verbose, 'r', 1, j, 0);
            info->nmoves++;
            info->weight += fw_r(1, j, p->size);


            op_prefix_reversal(p, next_strip);
            print_verbose(p, verbose, 'r', 1, next_strip , 0);
            info->nmoves++;
            info->weight += fw_r(1, next_strip, p->size);

          }else{
            op_reversal(p, i, next_strip);
            print_verbose(p, verbose, 'r', i, next_strip, 0);
            info->nmoves++;
            info->weight += fw_r(i, next_strip, p->size);
          }

        }
    }

}/*}}}*/
