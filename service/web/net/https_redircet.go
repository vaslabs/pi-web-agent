package net

import (
	"log"
	"net"
	"net/http"
	"strconv"
)

func RedirectToHTTPS(httpAddr string, tlsPort uint32) {
	httpSrv := http.Server{
		Addr: httpAddr,
		Handler: http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			host, _, _ := net.SplitHostPort(r.Host)
			u := r.URL
			u.Host = net.JoinHostPort(host, strconv.FormatUint(uint64(tlsPort), 10))
			u.Scheme = "https"
			log.Println("Redirecting http request to:", u.String())
			http.Redirect(w, r, u.String(), http.StatusMovedPermanently)
		}),
	}
	log.Println(httpSrv.ListenAndServe())
}
