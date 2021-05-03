package main

import (
	"bufio"
	"io"
	"testing"

	shell "github.com/vaslabs/pi-web-agent/internal"
)

func TestRunCommandWithOutput(t *testing.T) {
	t.Log("Starting command")

	reader, err := shell.RunWithOutput("echo", "hello", "hello")
	t.Log("Started command")
	if err != nil {
		t.Fatalf("Error executing command %s", err.Error())
	}

	buff_reader := bufio.NewReader(reader)

	for {
		line, err := buff_reader.ReadString('\n')
		if err != nil && err != io.EOF {
			t.Errorf("Error parsing package line %s . Delete %s\n", line, err)
			break
		} else if err == io.EOF {
			break
		}
		t.Logf("%s\n", line)
	}
}
