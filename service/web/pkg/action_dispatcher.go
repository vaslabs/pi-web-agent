package api

import (
	"fmt"
	"io"
	"log"

	"github.com/spf13/viper"
	net "github.com/vaslabs/pi-web-agent/net"
)

type Action interface {
	Action_Type() string
	execute(session *net.Session)
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

type system_info_response struct {
	OS_Info     Os_Info_Response
	Temperature string
	Kernel      string
}

func (display_live_info *Display_Live_Info) execute(session *net.Session) {
	os_info := OS_Info()
	temperature := Measure_Temperature()
	kernel_info := Kernel_Info()
	message := system_info_response{
		os_info,
		temperature.Temp,
		kernel_info,
	}
	session.Send(message)
}

func Parse_Action(r *io.Reader) (Action, error) {
	json_reader := viper.New()
	json_reader.SetConfigType("json")
	reader := (*r)
	err := json_reader.ReadConfig(reader)
	if err != nil {
		return nil, &UnparseableAction{err}
	}
	action_type := json_reader.GetString("Action_Type")
	if action_type == DISPLAY_LIVE_INFO {
		return &Display_Live_Info{}, nil
	} else {
		return nil, &UnrecognisedAction{action_type}
	}
}

func CreateDispatcher() net.Dispatcher {
	return func(session *net.Session, r *io.Reader) {
		action, error := Parse_Action(r)
		if (error != nil) {
			log.Fatalf("Error parsing next action %s", error.Error())
		} else {
			action.execute(session)
		}
	}
}