
run-backend: build-backend
	cd service/web && go run cmd/pi-web-agent.go || cd -

run-frontend: 
	cd ui/pi-web-agent-app && ng serve || cd -

build: build-dev-ui build-backend

test-backend:
	cd service/web && go test ./test/ && cd -

build-dev-ui:
	cd ui/pi-web-agent-app && npm i && ng build --base-href / && cd -

build-backend:
	cd service/web && go build -o pi-web-agent cmd/pi-web-agent.go && cd -

install-dev:
	sudo apt-get update && sudo apt-get install git && curl -L https://git.io/vQhTU | bash -s -- --version 1.16

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
	cd ui/pi-web-agent-app && npm i && ng build --prod --base-href / && cd -
	
build-rpi-backend:
	cd service/web && env GOOS=linux GOARCH=arm GOARM=5 go build -o pi-web-agent cmd/pi-web-agent.go && cd -

build-rpi: build-rpi-ui build-rpi-backend

package-rpi: build-rpi
	./package.sh

package_debian: package-rpi
	
