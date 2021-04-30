package shell

import (
	"bufio"
	"bytes"
	"io"
	"log"
	"os/exec"
)

func RunWithInput(input *bytes.Buffer, out *bytes.Buffer, command string, arg ...string) {
	cmd := exec.Command(command, arg...)
	cmd.Stdin = bufio.NewReader(input)
	cmd.Stdout = out
	cmd.Run()
}

func RunWithOutput(out *io.Writer, command string, arg ...string) {
	cmd := exec.Command(command, arg...)
	cmd.Stdout = *out
	err := cmd.Run()
	if err != nil {
		log.Printf("Error running command %s, %v", command, arg)
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
