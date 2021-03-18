# Description

This is a web-app agent for the raspberry pi. It allows you to interact easily with your Pi via your browser. 


# Raspbian Jessie

Get release from:

https://github.com/vaslabs/pi-web-agent/releases/tag/0.5


# Raspbian Wheezy
Get release from:

https://github.com/vaslabs/pi-web-agent/releases/tag/0.4-rc-2

This is the last release that supports Raspbian Wheezy


# How to install

ssh to your pi and wget the release zip. E.g. for 0.5 do:
```shell
wget https://github.com/vaslabs/pi-web-agent/archive/0.5.zip
```
Then unzip the downloaded file and go to the unzipped directory. Then run install.sh.
E.g. for the above example:
```shell
unzip 0.5.zip
cd 0.5
./install.sh
```
# Troubleshooting
There's been a report about the cgi daemon not starting. The following commands solve the issue.
```
sudo a2dismod mpm_event
sudo a2enmod mpm_prefork
sudo service pi-web-agent restart

sudo a2enmod cgi

service pi-web-agent restart
```

Installation not working:
- a2dismod not found:
```
sudo apt-get install apache2
```

- Due to a comment in Apache config:
Open the file and remove the comment on line 42

