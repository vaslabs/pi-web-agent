package api

import (
	shell "github.com/vaslabs/pi-web-agent/internal"
)

type power_off_response struct {
	message   string
	exit_code int32
}

func power_off() power_off_response {
	message, err := shell.RunSingle("poweroff")
	exit_code := 0
	if err == nil {
		exit_code = 1
	}
	return power_off_response{
		message:   message,
		exit_code: int32(exit_code),
	}
}
