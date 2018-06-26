#include <pthread.h>
#include <assert.h>

int i=1, j=1, i_calls =0, j_calls = 0;
#define NUM 5

int t1_l01(int i, int j){return 0;}
int t1_l02(int i, int j){return 0;}
int t2_l01(int i, int j){return 0;}
int t2_l02(int i, int j){return 0;}
int t1_inloop01(int i, int j){return 0;}
int t1_inloop02(int i, int j){return 0;}
int t2_inloop01(int i, int j){return 0;}
int t2_inloop02(int i, int j){return 0;}

int read_i(){
  i_calls++;
  return i;
}

void write_i(int x){
  i = x;
  i_calls++;
}


int read_j(){
  j_calls++;
  return j;
}

void write_j(int x){
  j = x;
  j_calls++;
}


void *t1(void* arg)
{
  int k = 0;
  t1_l01(i,j);
  for (k = 0; k < NUM; k++){
    t1_inloop01(i,j);
    write_i(read_i()+read_j());
    t1_inloop02(i,j);

  }
  t1_l02(i,j);
  return NULL;	
}


void *t2(void* arg)
{
  int k = 0;
  t2_l01(i,j);
  for (k = 0; k < NUM; k++){
    t2_inloop01(i,j);
    write_j(read_i()+read_j());
    t2_inloop02(i,j);

  }
  t2_l02(i,j);

  return NULL;

}

int main(int argc, char **argv)
{
  pthread_t id1, id2;

  pthread_create(&id1, NULL, t1, NULL);
  pthread_create(&id2, NULL, t2, NULL);

  pthread_join(id1, NULL);
  pthread_join(id2, NULL);

  if (i > 144 || j > 144) {
#if 0
    goto ERROR;
    ERROR:
      assert(0);
      ;
#endif
  }

  return 0;
}
/*
 * Daikon output
 * Num inv: 24
 * Num True: 14
 * Num False: 10
 * 
===========================================================================
..main():::ENTER
True: init
::i == ::j
True: init
::i == argc
True: init
::i == 1
True
argv has only one value
===========================================================================
..main():::EXIT
False: could not be these values depending on interleaving
::i == 6
False: could not be these values depending on interleaving
::j == 31
True: const
return == 0
===========================================================================
..t1():::ENTER
True: sees main's init
::i == ::j
True: sees main's init
::i == 1
True: const
arg == null
===========================================================================
..t1():::EXIT
False: j could be incremented
::j == orig(::i)
False: j could be incremented
::j == orig(::j)
True: const
return == orig(arg)
False: could change depending on if thread2 is always running concurrently
::i == 6
False: could change depending on if thread2 is always running concurrently
::j == 1
True: const
return == null
===========================================================================
..t2():::ENTER
False: could be 1
::i == 6
True: always 1 
::j == 1
True: const
arg == null
===========================================================================
..t2():::EXIT
False: could be modified
::i == orig(::i)
True: const
return == orig(arg)
False: could be larger
::i == 6
False: could be larger
::j == 31
True: const
return == null
*/
