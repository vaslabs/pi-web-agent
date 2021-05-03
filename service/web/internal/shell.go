package shell

import (
	"io"
	"log"
	"os/exec"
)

func RunWithOutput(command string, arg ...string) (io.ReadCloser, error) {
	cmd := exec.Command(command, arg...)
	log.Printf("Running %s %v", command, arg)
	reader, err := cmd.StdoutPipe()
	if err == nil {
		return reader, cmd.Start()
	} else {
		return reader, err
	}
}

func RunSingle(command string, arg ...string) (string, error) {
	out, err := exec.Command(command, arg...).Output()
	if err != nil {
		log.Printf("Error executing command %s: %s", command, err.Error())
		return "", err
	}
	return string(out), err
}
