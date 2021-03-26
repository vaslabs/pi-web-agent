package api

import (
	"log"
	shell "github.com/vaslabs/pi-web-agent/internal"
)

type os_info_response struct {
	Id               string ""
	Version_Id       string ""
	Version_Codename string ""
}

func OS_Info() os_info_response {
	return OS_Info_From("/etc", "os-release")
}

func OS_Info_From(path string, filename string) os_info_response {
	config, err := shell.Read_Env_Config(path, filename)
	if err != nil {
		log.Fatalf("Error %s", err.Error())
		return os_info_response{}
	} else {
		return os_info_response{
			config.GetString("ID"),
			config.GetString("VERSION_ID"),
			config.GetString("VERSION_CODENAME"),
		}
	}
}
