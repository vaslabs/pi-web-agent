echo "Starting pi-web-agent service"
sudo /etc/init.d/pi-web-agent start || exit 1
hostname=$(/usr/libexec/pi-web-agent/scripts/hostname.sh)
echo "Access the application via your browser on any machine from your lan:"
echo "Address is: https://$hostname:8003 for any machine on your lan"
echo "http://$hostname:8004 for a browser inside your Pi"
read a
