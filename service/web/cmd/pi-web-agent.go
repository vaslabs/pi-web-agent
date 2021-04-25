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
	config := single_user_session.PWA_Config
	addr := fmt.Sprintf(":%d", config.Port())
	tls_addr := fmt.Sprintf(":%d", config.TLS_Port())
	key_path := config.TLS_Key_File()
	cert_path := config.TLS_Cert_File()

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
	if _, err := os.Stat(key_path); err == nil {
		log.Println("Redirecting from ", addr)
		go net.RedirectToHTTPS(addr, config.TLS_Port())
		log.Println("Serving over TLS on ", tls_addr)
		log.Fatal(
			http.ListenAndServeTLS(
				tls_addr,
				cert_path,
				key_path,
				nil,
			),
		)
	} else {
		log.Println("Listening to ", addr)
		log.Fatal(http.ListenAndServe(addr, nil))
	}

}
