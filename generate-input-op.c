#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define _GNU_SOURCE
#include <getopt.h>
#include <math.h>

void opReversal(int size, int* pi, int i, int j, int isUnsigned){

    int * copy = malloc((size + 1) * sizeof (int));
    memcpy(copy, pi, (size + 1) * sizeof(int));

    int x, y = j;
    for(x = i; x <= j; x++){
        if(isUnsigned){
            pi[x] = copy[y];
        }else{
            pi[x] = -copy[y];
        }
        y--;
    }

    free(copy);
}


void opTransposition(int size, int* pi, int i, int j, int k){

    int * copy = malloc((size + 1) * sizeof (int));
    memcpy(copy, pi, (size + 1) * sizeof(int));


    int a = i, b = i+(k-j);

    while(a <= j-1){
        pi[b] = copy[a];
        a++;
        b++;
    }

    a = j;
    b = i;
    while(a <= k-1){
        pi[b] = copy[a];
        a++;
        b++;
    }
    free(copy);

}

void print(int size, int *permutation){
    int i;
    for (i = 1; i < size; i++) {
        printf("%d,", permutation[i]);
    }
    printf("%d\n", permutation[size]);
}

void generateOp(int size, int *i, int *j, int *k, int isUnsigned, char* alg){

    int isReversal;
    if(!strcmp(alg, "r")){
        isReversal = 1;
    }else if(!strcmp(alg, "t")){
        isReversal = 0;
    }else{
        isReversal = rand() % 2;
    }

    if(isReversal == 1){
        *i = 1 + (rand() % (size - isUnsigned));//if it is unsigned i < n
        if(isUnsigned){
          *j = *i + 1 + (rand() % (size - *i));
        }else{
          *j = *i + (rand() % (size - *i + 1));
        }
    }else{
        *i = 1 + (rand() % (size - 1));
        *j = *i + 1 + (rand() % (size - *i));
        *k = *j + 1 + (rand() % (size+1 - *j));
    }

}

int main(int argc, char *argv[]){
    extern char *optarg;
    char op;
    int size = 15, nperms = 50, nop = 1, uns = 1;
    int n, m;
    int *permutation, *identity;
    char * alg = "r";
    struct option longopts[] = {
        {"size", 1, NULL, 'n'},
        {"nperms", 1, NULL, 'q'},
        {"nop", 1, NULL, 'o'},
        {"uns", 1, NULL, 'u'},
        {"alg", 1, NULL, 'a'},
        {"help", 0, NULL, 'h'}
    };

    while ((op = getopt_long(argc, argv, "n:q:o:u:a:h", longopts, NULL)) != -1) {/*{{{*/

        switch (op) {
            case 'n':
                size = atoi(optarg);
                break;
            case 'q':
                nperms = atoi(optarg);
                break;
            case 'o':
                nop = atoi(optarg);
                break;
            case 'u':
                uns = atoi(optarg);
                break;
            case 'a':
                alg = optarg;
                break;
            case 'h':
                printf("usage: %s [options] \n", argv[0]);
                printf("options: \n");
                printf("\t--size or -n: permutation size (default = 15)\n");
                printf("\t--nop or -o: number of random operations to apply (default = 10)\n");
                printf("\t--uns or -u: 1 for unsigned and - for signed (default = 1)\n");
                printf("\t--alg or -a: algorithm (default = r)\n");
                printf("\t--nperms or -q: number of permutations to be created (default = 50)\n");
                exit(0);
        }
    }/*}}}*/

    permutation = malloc((size + 1) * sizeof (int));
    identity = malloc((size + 1) * sizeof (int));


    for(m = 0; m<= size; m++){
        identity[m] = m;
    }
    for (n = 0; n < nperms; n++) {
        memcpy(permutation, identity, (size + 1) * sizeof(int));

        for(m = 0; m < nop; m++){
            int i,j,k= 0;
            generateOp(size, &i, &j, &k, uns, alg);
            // printf("%d, %d, %d\n", i, j, k);
            if(k > 0){
                opTransposition(size, permutation, i, j, k);
            }else{
                opReversal(size, permutation, i, j, uns);
            }
            // print(size, permutation);
        }
        print(size, permutation);
    }

    free(identity);
    free(permutation);
}
