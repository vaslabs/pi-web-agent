package main

import (
	"io"
	"log"
	"net/http"
	api "github.com/vaslabs/pi-web-agent/pkg"
	"encoding/json"
)

type system_info_response struct {
	OS_Info api.Os_Info_Response
	Temperature api.Temperature_Response
}

func system_info_handler(w http.ResponseWriter, req *http.Request) {
	os_info := api.OS_Info()
	temperature := api.Measure_Temperature()
	json.NewEncoder(w).Encode(system_info_response{
		os_info,
		temperature,
	})
}

func main() {

	api_action_prefix := "/api/action/"
	api_info_prefix := "/api/info/"

	dummyHandler := func(w http.ResponseWriter, req *http.Request) {
		io.WriteString(w, "Hello, world!\n")
	}
	// Simple static webserver:
	http.HandleFunc(api_action_prefix, dummyHandler)
	http.HandleFunc(api_info_prefix + "os_info", system_info_handler)
	http.Handle("/assets/", http.FileServer(http.Dir("assets")))

	log.Fatal(http.ListenAndServe(":8080", nil))
}
