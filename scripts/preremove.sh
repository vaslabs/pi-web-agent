echo "Attempting to stop piwebagent2.service"
systemctl stop piwebagent2.service || echo "Failed to stop"
echo "Attempting to disable piwebagent2.service"
systemctl disable piwebagent2.service || echo "Failed to disable"