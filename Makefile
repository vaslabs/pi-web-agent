
run-backend: build-backend
	cd service/web && go run cmd/pi-web-agent.go || cd -

run-frontend: 
	cd ui/pi-web-agent-app && ng serve || cd -

build: build-dev-ui build-backend

test-backend:
	cd service/web && go test ./test/ && cd -

build-dev-ui:
	cd ui/pi-web-agent-app && npm i && ng build --base-href / && cd -
	cp -r ui/pi-web-agent-app/dist/pi-web-agent-app service/web/assets/

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