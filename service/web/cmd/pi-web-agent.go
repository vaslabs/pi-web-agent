package main

import (
	"fmt"
	"io"
	"log"
	"net/http"

	net "github.com/vaslabs/pi-web-agent/net"
	api "github.com/vaslabs/pi-web-agent/pkg"
)

func main() {

	single_user_session := net.NewSession()

	api_action_prefix := "/api/action/"

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

	addr := fmt.Sprintf(":%d", single_user_session.PWA_Config.Port())

	log.Fatal(http.ListenAndServe(addr, nil))
}
