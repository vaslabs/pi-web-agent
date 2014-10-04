#include <stdio.h>
#include <stdlib.h>

void printContent(FILE *ifp) {
    int c;
    do
    {
        c = fgetc(ifp);
        if( feof(ifp) )
        {
          break ;
        }
        printf("%c", (char)c);
    }while(1);
   
   fclose(ifp);
}

void outputContent(FILE *ifp) {
    printf("Content-type: application/json\n\n");
    
    printContent(ifp);
}

