#include "/usr/libexec/pi-web-agent/etc/config/framework.c"

int main() {
    
    FILE *fileExtensions, *fileActions;
    char *mode = "r";

    fileExtensions = fopen("/usr/libexec/pi-web-agent/etc/config/config.cfg", mode);
    fileActions = fopen("/usr/libexec/pi-web-agent/etc/config/.actions", mode);
    
    printf("Content-type: application/json\n\n");
    printf("[\n");
    printContent(fileExtensions);
    printf(",\n");
    printContent(fileActions);
    printf("]\n");
    
    return 0; 
}
