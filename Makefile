
run-backend: build-backend
	cd service/web && go run cmd/pi-web-agent.go || cd -

build: build-dev-ui build-backend

test-backend:
	cd service/web && go test ./test/ && cd -

build-dev-ui:
	cd ui/pi-web-agent-app && npm i && ng build --base-href / && cd -
	cp -r ui/pi-web-agent-app/dist/pi-web-agent-app service/web/assets/

build-backend:
	cd service/web && go build -o pi-web-agent cmd/pi-web-agent.go && cd -

clean:
	rm -r service/web/assets/pi-web-agent-app