![sanity build](https://github.com/vaslabs/pi-web-agent/actions/workflows/sanity.yml/badge.svg?branch=remaster)

# Description

This is a web-app agent for the Raspberry Pi. It allows you to interact easily with your Pi via your browser.

# How to install

## Early adapters

On your raspberry pi download and install the latest 0.7.x debian package from
from https://github.com/vaslabs/pi-web-agent/releases .

You're probably gonna need the arm.deb one (not the arm64)

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

### Dev Environment Wrapper

Given that you have all dependencies setup on your machine
rpi in your `/etc/hosts` and `.ssh/config` entry for `pi` user
called `rpi` you can run `./dev.sh` to spin a reloadable front-end with
current backend build.

If you you update backend just `ctrl-c` and run `./dev.sh` again

The dev app is accessible to your lan via your local ip since dev server
listens to `0.0.0.0`.
(and to the public via your public ip if you did any port forwarding
to your machine)

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
