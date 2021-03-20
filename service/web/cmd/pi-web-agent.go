package main

import (
	"log"
	"net/http"
	"io"
)



func main() {

	dummyHandler := func(w http.ResponseWriter, req *http.Request) {
		io.WriteString(w, "Hello, world!\n")
	}
	// Simple static webserver:
	http.Handle("/assets/", http.FileServer(http.Dir("assets")))
	http.HandleFunc("/action/", dummyHandler)
	log.Fatal(http.ListenAndServe(":8080", nil))
}
