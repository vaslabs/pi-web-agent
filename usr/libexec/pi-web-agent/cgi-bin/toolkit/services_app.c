#include <stdio.h>
#include <stdlib.h>

int main() {
    
    FILE *ifp, *ofp;
    char *mode = "r";

    ifp = fopen("/usr/libexec/pi-web-agent/templates/services_controller.htm", mode);

    if (ifp == NULL) {
        fprintf(stderr, "Failed to open template file!\n");
        exit(1);
    }

    int c;
    printf("Content-type: text/html\n\n");
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
   return 0; 

}
