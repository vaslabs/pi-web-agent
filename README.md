![sanity build](https://github.com/vaslabs/pi-web-agent/actions/workflows/sanity.yml/badge.svg?branch=remaster)


# Description

This is a web-app agent for the raspberry pi. It allows you to interact easily with your Pi via your browser. 


# How to install

## Early adapters
On your raspberry pi download and install pi-web-agent_0.7.0_linux_arm.deb
from https://github.com/vaslabs/pi-web-agent/releases/tag/0.7.0

This is a pre release. For any ideas let us know https://github.com/vaslabs/pi-web-agent/discussions
For any issues feel free to report here https://github.com/vaslabs/pi-web-agent/issues

We are not supporting the old version anymore, all hands are to build a brand new pi-web-agent that's easy to maintain and for users to install and use with minimal to zero dependencies.

## Devs only

### Pre-requisites

- [pre-commit](https://pre-commit.com/)
- [golang](https://golang.org/)
- npm
- [angular](https://angular.io/)

### Back-End development
The service will be communicating via a websocket. To test the service without
FE you can use https://chrome.google.com/webstore/detail/smart-websocket-client/omalebghpgejjiaoknljcfmglgbpocdp/related?utm_source=chrome-app-launcher-info-dialog

#### Setup hook
```
make check-hook
```

#### Run app

```
make run-backend
```

#### Run tests
```
make test-backend
```

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

# Old versions


## Raspbian Jessie

Get release from:

https://github.com/vaslabs/pi-web-agent/releases/tag/0.5


## Raspbian Wheezy
Get release from:

https://github.com/vaslabs/pi-web-agent/releases/tag/0.4-rc-2

This is the last release that supports Raspbian Wheezy
