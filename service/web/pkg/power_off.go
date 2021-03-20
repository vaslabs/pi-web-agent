package power_management

import (
	"vaslabs.org/pi-web-agent/internal/shell"
)

type power_off_response struct {
	message   string
	exit_code int32
}

func power_off() power_off_response {
	message, err := shell.RunSinle("poweroff")
	exit_code := 0
	if err == nil {
		exit_code  = 1
	}
	return power_off_response{
		message: message,
		exit_code: int32(exit_code),
	}
}
