package main

import (
	"io"
	"strings"
	"testing"

	api "github.com/vaslabs/pi-web-agent/pkg"
)

func Test_Live_Info_Action(t *testing.T) {
	json := "{\"action_type\": \"DISPLAY_LIVE_INFO\"}"

	reader := io.Reader(strings.NewReader(json))
	action, err := api.Parse_Action(&reader)
	if err != nil {
		t.Errorf("Test failure %s", err.Error())
	}
	if action.Action_Type() != api.DISPLAY_LIVE_INFO {
		t.Errorf("Expected %s but got %s", api.DISPLAY_LIVE_INFO, action.Action_Type())
	}

	json = "{\"action_type\": \"APPLY_UPDATES\"}"
	reader = io.Reader(strings.NewReader(json))
	action, err = api.Parse_Action(&reader)
	if (action.Action_Type() != api.APPLY_UPDATES) {
		t.Errorf("Expected %s but got %s", api.APPLY_UPDATES, action.Action_Type())
	}
}
