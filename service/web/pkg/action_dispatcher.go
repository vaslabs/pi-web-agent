package api

import (
	"bufio"
	"bytes"
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

type Power_Off struct {
}

type Reboot struct {
}

type Set_Passphrase struct {
	Passphrase string
}

type Find_Available_Updates struct{}

type Apply_Updates struct{}

const DISPLAY_LIVE_INFO = "DISPLAY_LIVE_INFO"
const REBOOT = "REBOOT"
const POWER_OFF = "POWER_OFF"
const SET_PASSPHRASE = "SET_PASSPHRASE"
const AVAILABLE_UPDATES = "AVAILABLE_UPDATES"
const APPLY_UPDATES = "APPLY_UPDATES"

func (c *Display_Live_Info) Action_Type() string {
	return DISPLAY_LIVE_INFO
}

func (apply_updates *Apply_Updates) Action_Type() string {
	return APPLY_UPDATES
}

func (r *Reboot) Action_Type() string {
	return REBOOT
}
func (p *Power_Off) Action_Type() string {
	return POWER_OFF
}

func (p *Set_Passphrase) Action_Type() string {
	return SET_PASSPHRASE
}

func (available_updates *Find_Available_Updates) Action_Type() string {
	return AVAILABLE_UPDATES
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

func (reboot *Reboot) execute(session *net.Session) {
	session.Send(System_Reboot())
}

func (power_off *Power_Off) execute(session *net.Session) {
	session.Send(System_Power_Off())
}

func (set_pass *Set_Passphrase) execute(session *net.Session) {
	session.Set_Pass(set_pass.Passphrase)
}

func (available_updates *Find_Available_Updates) execute(session *net.Session) {
	session.Send(Available_Updates())
}

func (apply_updates *Apply_Updates) execute(session *net.Session) {
	buffer := bytes.NewBuffer(make([]byte, 1024))
	out := io.Writer(buffer)
	defer Update(&out)
	reader := bufio.NewReader(buffer)
	session.SendMultiple(reader)
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
	switch action_choice := action_type; action_choice {
	case DISPLAY_LIVE_INFO:
		return &Display_Live_Info{}, nil
	case REBOOT:
		return &Reboot{}, nil
	case POWER_OFF:
		return &Power_Off{}, nil
	case AVAILABLE_UPDATES:
		return &Find_Available_Updates{}, nil
	case APPLY_UPDATES:
		return &Apply_Updates{}, nil
	default:
		return nil, &UnrecognisedAction{action_type}
	}

}

func CreateDispatcher() net.Dispatcher {
	return func(session *net.Session, r *io.Reader) {
		action, error := Parse_Action(r)
		if error != nil {
			log.Printf("Error parsing next action %s", error.Error())
		} else {
			action.execute(session)
		}
	}
}
