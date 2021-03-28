![sanity build](https://github.com/vaslabs/pi-web-agent/actions/workflows/sanity.yml/badge.svg?branch=remaster)


# Description

This is a web-app agent for the raspberry pi. It allows you to interact easily with your Pi via your browser. 


# How to install

## Devs only

### Pre-requisites
- [pre-commit](https://pre-commit.com/) (pip install -U pre-commit)
- npm

### Front-End development

Associate pi web agent address with the name `rpi` in `/etc/hosts`

For example:
```
192.168.0.12 rpi
```
(that name is used to proxy requests to your raspberry pi)

```
cd ui/pi-we-agent-app
npm start
```

### Build

```
make build
```

### Pre-Commit
Before doing you first commit run precommit install
Running pre-commit hooks locally ensures you keep up with basic project setup/standards and gives you the chance to fix anything needed before committing your code
 
# Old versions


## Raspbian Jessie

Get release from:

https://github.com/vaslabs/pi-web-agent/releases/tag/0.5


## Raspbian Wheezy
Get release from:

https://github.com/vaslabs/pi-web-agent/releases/tag/0.4-rc-2

This is the last release that supports Raspbian Wheezy
