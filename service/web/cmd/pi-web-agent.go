package main

import (
	"encoding/json"
	"io"
	"log"
	"net/http"

	api "github.com/vaslabs/pi-web-agent/pkg"
)

type system_info_response struct {
	OS_Info     api.Os_Info_Response
	Temperature string
	Kernel      string
}

func system_info_handler(w http.ResponseWriter, req *http.Request) {
	os_info := api.OS_Info()
	temperature := api.Measure_Temperature()
	kernel_info := api.Kernel_Info()
	json.NewEncoder(w).Encode(system_info_response{
		os_info,
		temperature.Temp,
		kernel_info,
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
	http.HandleFunc(api_info_prefix+"os_info", system_info_handler)
	http.Handle("/assets/", http.FileServer(http.Dir("assets")))

	log.Fatal(http.ListenAndServe(":8080", nil))
}
