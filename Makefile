
CC = gcc
CFLAGS = -ggdb -Wall -pedantic
OBJS = util.o rearrangements.o permutations.o breakpoints.o approx/wt.o approx/wr.o approx/wsr.o approx/wr_g.o approx/wsr_g.o approx/wt_g.o approx/wrt_g.o approx/wsrt_g.o
BIN = prog
BIN_LB = prog_lb
BIN_ONEPERM = prog_o
file: $(OBJS) main-file.o
	$(CC) -o $(BIN) $(CFLAGS) $(OBJS) main-file.o -lm

lb: $(OBJS) main-lb.o
	$(CC) -o $(BIN_LB) $(CFLAGS) $(OBJS) main-lb.o -lm

oneperm: $(OBJS) main-one-prm.o
	$(CC) -o $(BIN_ONEPERM) $(CFLAGS) $(OBJS) main-one-prm.o -lm

generate-signed: $(OBJS) generate-signed.o
	$(CC) -o generate-signed $(CFLAGS) $(OBJS) generate-signed.o -lm

generate-small-signed: $(OBJS) generate-small-signed.o
	$(CC) -o generate-small-signed $(CFLAGS) $(OBJS) generate-small-signed.o -lm

generate-small-unsigned: $(OBJS) generate-small-unsigned.o
	$(CC) -o generate-small-unsigned $(CFLAGS) $(OBJS) generate-small-unsigned.o -lm

generate-unsigned: $(OBJS) generate-unsigned.o
	$(CC) -o generate-unsigned $(CFLAGS) $(OBJS) generate-unsigned.o -lm

generate-input-op: $(OBJS) generate-input-op.o
	$(CC) -o generate-input-op $(CFLAGS) $(OBJS) generate-input-op.o -lm

clean:
	rm *.o approx/*.o
