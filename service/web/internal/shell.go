package shell

import (
	"bufio"
	"bytes"
	"log"
	"os/exec"
)

func RunWithInput(input *bytes.Buffer, command string, arg ...string) *bytes.Buffer {
	cmd := exec.Command(command, arg...)
	cmd.Stdin = bufio.NewReader(input)
	var out bytes.Buffer
	cmd.Stdout = &out
	return &out
}

func RunBufferedOutput(input *bytes.Buffer, command string, arg ...string) *bytes.Buffer {
	cmd := exec.Command(command, arg...)
	var out bytes.Buffer
	cmd.Stdout = &out
	return &out
}

func RunSingle(command string, arg ...string) (string, error) {
	out, err := exec.Command(command, arg...).Output()
	if err != nil {
		log.Fatal(err)
		return "", err
	}
	return string(out), err
}
