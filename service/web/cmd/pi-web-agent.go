package main

import (
	"io"
	"log"
	"net/http"
	api "github.com/vaslabs/pi-web-agent/pkg"
	"encoding/json"
)

func os_info_handler(w http.ResponseWriter, req *http.Request) {
	os_info := api.OS_Info()
	json.NewEncoder(w).Encode(os_info)
}

func main() {

	api_action_prefix := "/api/action/"
	api_info_prefix := "/api/info/"

	dummyHandler := func(w http.ResponseWriter, req *http.Request) {
		io.WriteString(w, "Hello, world!\n")
	}
	// Simple static webserver:
	http.HandleFunc(api_action_prefix, dummyHandler)
	http.HandleFunc(api_info_prefix + "os_info", os_info_handler)
	http.Handle("/assets/", http.FileServer(http.Dir("assets")))

	log.Fatal(http.ListenAndServe(":8080", nil))
}
