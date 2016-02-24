#include "proc/sysinfo.h"
#include "proc/procps.h"
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/statvfs.h>
#include <sys/types.h>
#include <sys/utsname.h>
#include <unistd.h>
#include <ifaddrs.h>

#define _GNU_SOURCE     /* To get defns of NI_MAXSERV and NI_MAXHOST */
#include <arpa/inet.h>
#include <sys/socket.h>
#include <netdb.h>
#include <linux/if_link.h>

#define TRUE "true"
#define FALSE "false"
#define fname_update "/var/log/pi-update/pi_packages_update"
int main(int argc, char *argv[]) {

    printf("Content-type: text/json\n\n");
    struct sysinfo memory;
    struct statvfs disk;
    struct utsname unameinfo;
    (&memory)->mem_unit=2;
    
   if (sysinfo((&memory)) != 0)
        return 1;
    
    if (statvfs("/", &disk) != 0) {
        return 1;
    }
    
    if (uname(&unameinfo) != 0) {
        return 1;
    }

    printf("{\n\"mem\":%.2f, \"swap\":%.2f,\n",
        1-(((&memory)->freeram+(&memory)->bufferram+(&memory)->sharedram)/(double)((&memory)->totalram)),
        1-(&memory)->freeswap/(double)((&memory)->totalswap)
    );

    printf("\"disk\":%.2f,\n", 1-disk.f_bfree/(double)(disk.f_blocks));
    char hostname[64];
    gethostname(hostname, 64);
    printf("\"kernel\":\"%s\", \"hostname\":\"%s\",\n", unameinfo.release, hostname);
    printf("\"ucheck\":%s,\n", access(fname_update, F_OK) == 0 ? TRUE : FALSE);
    printf("\"ip\":");
    get_ip();
    get_temperature();
    printf("}\n");
    return 0;
}

int get_temperature() {
    FILE *temperatureFile;
    double T;
    temperatureFile = fopen ("/sys/class/thermal/thermal_zone0/temp", "r");
    if (!temperatureFile) {
      printf(",\n");
      printf ("\"temp\": null");
      return;
    }
    fscanf (temperatureFile, "%lf", &T);
    T /= 1000;
    printf(",\n");
    printf ("\"temp\":%.2f", T);
    fclose (temperatureFile);
}

int get_ip()
{
    struct ifaddrs *ifaddr, *ifa;
    int family, s, n;
    char host[NI_MAXHOST];

    if (getifaddrs(&ifaddr) == -1) {
       perror("getifaddrs");
       exit(EXIT_FAILURE);
    }

    /* Walk through linked list, maintaining head pointer so we
      can free list later */

    for (ifa = ifaddr, n = 0; ifa != NULL; ifa = ifa->ifa_next, n++) {
        if (ifa->ifa_addr == NULL)
            continue;

        family = ifa->ifa_addr->sa_family;

        /* Display interface name and family (including symbolic
           form of the latter for the common families) */


        /* For an AF_INET* interface address, display the address */

        if (family == AF_INET || family == AF_INET6) {
            s = getnameinfo(ifa->ifa_addr,
                    (family == AF_INET) ? sizeof(struct sockaddr_in) :
                                         sizeof(struct sockaddr_in6),
                    host, NI_MAXHOST,
                    NULL, 0, NI_NUMERICHOST);
            if (s != 0) {
                exit(EXIT_FAILURE);
            }
            if (strcmp(ifa->ifa_name, "eth0") == 0) {
                printf("{\"name\":\"%s\", \"address\":\"%s\"}\n", ifa->ifa_name, host);
                break;
            }
        }
    }      
    
    freeifaddrs(ifaddr);
}
