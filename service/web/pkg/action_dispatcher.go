package api

import (
	"fmt"
	"io"
	"github.com/spf13/viper"
)

type Action interface {
	Action_Type() string
}

type Display_Live_Info struct {
}

const DISPLAY_LIVE_INFO = "DISPLAY_LIVE_INFO"

func (c Display_Live_Info) Action_Type() string {
	return DISPLAY_LIVE_INFO
}

type UnrecognisedAction struct {
	action_type string
}

type UnparseableAction struct {
	err error
}

func (unrecognised_action *UnrecognisedAction) Error() string {
	return fmt.Sprintf("Unrecognised action type %s", unrecognised_action.action_type)
}

func (unparseable_action *UnparseableAction) Error() string {
	return fmt.Sprintf("Unparseable action due to %s", unparseable_action.err.Error())
}

func Parse_Action(r io.Reader) (Action, error) {
	json_reader := viper.New()
	json_reader.SetConfigType("json")
	err := json_reader.ReadConfig(r)
	if err != nil {
		return nil, &UnparseableAction{err}
	}
	action_type := json_reader.GetString("Action_Type")
	if action_type == DISPLAY_LIVE_INFO {
		return Display_Live_Info{}, nil
	} else {
		return nil, &UnrecognisedAction{action_type}
	}
}
