#include <stdio.h>
#include <stdlib.h>
#include <string.h>
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

void outputJSONContent(FILE *ifp) {
    printf("Content-type: application/json\n\n");
    
    printContent(ifp);
}

void outputHTMLContent(FILE *ifp) {
    printf("Content-type: text/html\n\n");
    
    printContent(ifp);
}


void outputTemplateH(char *template_name, int printHeaders) {
    FILE *ifp;
    char *mode = "r";
    char path[255];
    strcpy(path, "/usr/libexec/pi-web-agent/templates/");
    
    strcat(path, template_name);
    strcat(path, ".htm");
     
    ifp = fopen(path, mode);
    if (printHeaders == 1)
        outputHTMLContent(ifp);
    else 
        printContent(ifp);
}

void outputTemplate(char *template_name) {
    outputTemplateH(template_name, 1);
}

