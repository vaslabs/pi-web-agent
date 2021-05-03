
dev_pwa_root_path_prefix := /home/pi/pi-web-agent/service/system/
executables              := $(shell cat .executables)
dev_executables          := $(shell l="";for i in $$(cat .executables); do l="$$l $(dev_pwa_root_path_prefix)$$i"; done; echo $$l)
run-backend: build-rpi-backend
	    chmod +x service/web/pi-web-agent \
		&& rsync -a --exclude 'node_modules' . rpi:/home/pi/pi-web-agent \
		&& ssh rpi "/bin/bash -c '\
			sudo service piwebagent2 stop; \
			sudo killall -9 pi-web-agent; \
			export PWA_ROOT_PATH_PREFIX=\"$(dev_pwa_root_path_prefix)\"; \
			chmod +x $(dev_executables) ;\
			/home/pi/pi-web-agent/service/system/etc/cron.daily/update_check; \
			[ -z $$(cat $(dev_pwa_root_path_prefix)usr/lib/piwebagent2/update_check) ] \
			&& cp /home/pi/pi-web-agent/service/web/test/test-resources/update_check $(dev_pwa_root_path_prefix)usr/lib/piwebagent2/update_check; \
			/home/pi/pi-web-agent/service/web/pi-web-agent'; \
		"

run-frontend: 
	npm --prefix ui/pi-web-agent-app start || cd -

build: build-dev-ui build-backend

test-backend:
	cd service/web && go test ./test/ && cd -

build-dev-ui:
	npm --prefix ui/pi-web-agent-app i &&npm --prefix ui/pi-web-agent-app run ng build -- --base-href / 

build-backend:
	cd service/web && go build -o pi-web-agent cmd/pi-web-agent.go && cd -

install-dev:
	sudo apt-get update && sudo apt-get install git nodejs npm && curl -L https://git.io/vQhTU | bash -s -- --version 1.16

uninstall-go:
	curl -L https://git.io/vQhTU | bash -s -- --remove

clean:
	rm -r service/web/assets/pi-web-agent-app

check-hook:
	[ -f .git/hooks/pre-commit ] && echo "Hook ready" || pre-commit install || echo "Please install pre-commit (https://pre-commit.com/)" 

package-dev: build
	./package.sh

install: package-dev
	sudo ./install.sh

make uninstall:
	sudo ./uninstall.sh



build-rpi-ui:
	npm --prefix ui/pi-web-agent-app i \
		&&npm --prefix ui/pi-web-agent-app run ng build -- --prod --base-href / 
	
build-rpi-backend:
	cd service/web && env GOOS=linux GOARCH=arm GOARM=5 go build -o pi-web-agent cmd/pi-web-agent.go && cd -

build-rpi: build-rpi-ui build-rpi-backend

package-rpi: build-rpi
	./package.sh

package-debian: package-rpi
	./debian.sh
