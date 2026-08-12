#include <stdio.h>

#define Hi "\u203E"
#define Lo "_"
#define Un "*"  // Undefined
#define Im "x"  // High Impedence
#define Tr "|"  // Transition
#define Up "/"  // Up
#define Do "\\" // Down
#define NL "\n" // Newline

int main(){
  printf(Un Un Un Un Un Un Up Hi Hi Hi Hi Hi Do Lo Lo Lo Lo Lo NL);
}
