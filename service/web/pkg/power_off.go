package api

import (
	shell "github.com/vaslabs/pi-web-agent/internal"
)

type power_off_response struct {
	Message   string
	Exit_Code int32
}

func System_Power_Off() power_off_response {
	message, err := shell.RunSingle("poweroff")
	exit_code := 0
	if err == nil {
		exit_code = 1
	}
	return power_off_response{
		Message:   message,
		Exit_Code: int32(exit_code),
	}
}

func System_Reboot() power_off_response {
	message, err := shell.RunSingle("reboot")
	exit_code := 0
	if err == nil {
		exit_code = 1
	}
	return power_off_response{
		Message:   message,
		Exit_Code: int32(exit_code),
	}
}
