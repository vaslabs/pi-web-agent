#include "/usr/libexec/pi-web-agent/etc/config/framework.c"
int main() {
    outputTemplate("_main_part1");
    outputTemplateH(
        "package_recommendations_controller", 
        0
    );
    outputTemplateH("_main_part2", 0);
}
