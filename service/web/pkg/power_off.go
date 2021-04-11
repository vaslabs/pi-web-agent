package api

import (
	"syscall"
)

type power_off_response struct {
	Message   string
	Exit_Code int32
}

func System_Power_Off() power_off_response {
	err := syscall.Reboot(syscall.LINUX_REBOOT_CMD_POWER_OFF)
	message := "Powering off"
	exit_code := 0
	if err != nil {
		exit_code = 1
		message = err.Error()
	}
	return power_off_response{
		Message:   message,
		Exit_Code: int32(exit_code),
	}
}

func System_Reboot() power_off_response {
	err := syscall.Reboot(syscall.LINUX_REBOOT_CMD_RESTART)
	message := "Rebooting"
	exit_code := 0
	if err != nil {
		exit_code = 1
		message = err.Error()
	}
	return power_off_response{
		Message:   message,
		Exit_Code: int32(exit_code),
	}
}
