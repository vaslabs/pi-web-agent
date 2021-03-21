![sanity build](https://github.com/vaslabs/pi-web-agent/actions/workflows/sanity.yml/badge.svg?branch=remaster)


# Description

This is a web-app agent for the raspberry pi. It allows you to interact easily with your Pi via your browser. 


# How to install

## Devs only

### Pre-requisites

- npm
- angular (`npm install -g @angular/cli`)

### Front-End development

Associate pi web agent address with the name `rpi` in `/etc/hosts`

For example:
```
192.168.0.12 rpi
```
(that name is used to proxy requests to your raspberry pi)

```
cd ui/pi-we-agent
npm start
```

### Build

```
make build
```

# Old versions


## Raspbian Jessie

Get release from:

https://github.com/vaslabs/pi-web-agent/releases/tag/0.5


## Raspbian Wheezy
Get release from:

https://github.com/vaslabs/pi-web-agent/releases/tag/0.4-rc-2

This is the last release that supports Raspbian Wheezy
