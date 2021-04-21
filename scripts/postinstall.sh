
echo "Giving permissions to piwebagent to access its static content"
chown piwebagent2 /usr/share/piwebagent2/assets

echo "Enabling piwebagent2.service"
systemctl enable piwebagent2.service
echo "Starting piwebagent2.service"
systemctl start piwebagent2.service
