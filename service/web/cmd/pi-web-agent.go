package main

import (
	"fmt"
	"io"
	"log"
	"net/http"
	"os"

	net "github.com/vaslabs/pi-web-agent/net"
	api "github.com/vaslabs/pi-web-agent/pkg"
)

func main() {
	single_user_session := net.NewSession()
	addr := fmt.Sprintf(":%d", single_user_session.PWA_Config.Port())

	api_action_prefix := "/api/action/"
	key_path := "/etc/pwa_ca/rpi/key.pem"
	cert_path := "/etc/pwa_ca/rpi/cert.pem"

	dummyHandler := func(w http.ResponseWriter, req *http.Request) {
		io.WriteString(w, "Hello, world!\n")
	}
	action_dispatcher := api.CreateDispatcher()
	action_dispatcher_handler := func(w http.ResponseWriter, req *http.Request) {
		single_user_session.Open_Web_Socket(w, req, action_dispatcher)
	}
	// Simple static webserver:
	http.HandleFunc(api_action_prefix, dummyHandler)
	http.HandleFunc("/api/control/stream", action_dispatcher_handler)
	http.Handle("/", http.FileServer(http.Dir("assets")))
	if _, err := os.Stat(key_path); err == nil {
		log.Fatal(
			http.ListenAndServeTLS(
				":443",
				key_path,
				cert_path,
				nil,
			),
		)
	} else {
		log.Fatal(http.ListenAndServe(addr, nil))
	}

