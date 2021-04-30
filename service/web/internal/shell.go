package shell

import (
	"bufio"
	"bytes"
	"log"
	"os/exec"
)

func RunWithInput(input *bytes.Buffer, out *bytes.Buffer, command string, arg ...string) {
	cmd := exec.Command(command, arg...)
	cmd.Stdin = bufio.NewReader(input)
	cmd.Stdout = out
	cmd.Run()
}

func RunWithOutput(out *bytes.Buffer, command string, arg ...string) {
	cmd := exec.Command(command, arg...)
	cmd.Stdout = out
	cmd.Run()
}

func RunSingle(command string, arg ...string) (string, error) {
	out, err := exec.Command(command, arg...).Output()
	if err != nil {
		log.Printf("Error executing command %s: %s", command, err.Error())
		return "", err
	}
	return string(out), err
}
