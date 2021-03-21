package main

import (
	"io"
	"log"
	"net/http"
)

func main() {

	dummyHandler := func(w http.ResponseWriter, req *http.Request) {
		io.WriteString(w, "Hello, world!\n")
	}
	// Simple static webserver:
	http.HandleFunc("/action/", dummyHandler)
	http.Handle("/assets/", http.FileServer(http.Dir("assets")))

	log.Fatal(http.ListenAndServe(":8080", nil))
}
