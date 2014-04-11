#!/bin/bash
echo $(/sbin/ifconfig | grep "inet addr" |\
 grep -E -v "10.[0-9]?.[0-9]?.[0-9]" |\
 grep -v "127.0.0.1" | awk '{print $2}' |\
  awk -F: '{print $2 }' | tail -n 1)
