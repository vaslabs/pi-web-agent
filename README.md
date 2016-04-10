#Description

This is a web-app agent for the raspberry pi. It allows you to interact easily with your Pi via your browser. 


#Raspbian Jessie

Get release from:

https://github.com/vaslabs/pi-web-agent/releases/tag/0.4-rc-2_jessie

If you want to try out the pre-release of the new user interface get it from:

https://github.com/vaslabs/pi-web-agent/releases/tag/0.5_pre


#Raspbian Wheezy
Get release from:

https://github.com/vaslabs/pi-web-agent/releases/tag/0.4-rc-2

This is the last release that supports Raspbian Wheezy


# How to install

ssh to your pi and wget the release zip. E.g. for 0.5 do:
```shell
wget https://github.com/vaslabs/pi-web-agent/archive/0.5_pre.zip
```
Then unzip the downloaded file and go to the unzipped directory. Then run install.sh.
E.g. for the above example:
```shell
unzip 0.5_pre.zip
cd 0.5_pre
./install.sh
```
