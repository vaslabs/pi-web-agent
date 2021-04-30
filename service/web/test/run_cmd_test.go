package main

import (
	"bufio"
	"bytes"
	"io"
	"strings"
	"testing"

	shell "github.com/vaslabs/pi-web-agent/internal"
)

func TestRunCommandWithOutput(t *testing.T) {
	buffer := bytes.NewBuffer(make([]byte, 0))
	writer := io.Writer(buffer)
	reader := bufio.NewReader(buffer)
	shell.RunWithOutput(&writer, "echo", "hello\n", "hello2\n")

	l, _ := reader.ReadString('\n')
	firstLine := strings.Trim(strings.TrimSpace(l), "\x00")
	l, _ = reader.ReadString('\n')
	secondLine := strings.Trim(strings.TrimSpace(l), "\x00")

	expected := "hello"

	if firstLine != expected {
		t.Errorf("Expected '%s' but got '%s'", expected, firstLine)
	}

	expected = "hello2"

	if secondLine != expected {
		t.Errorf("Expected %s but got '%s'", expected, secondLine)
	}
}
