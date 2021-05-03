userdel piwebagent2 || echo "Could not remove piwebagent2 user"
rm -r /etc/pwa_ca || echo "Could not remove piwebagent2 certificates"
groupdel pwassl || echo "Could not remove pwassl"
