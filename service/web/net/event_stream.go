package net

import (
	"log"
	"net/http"
	"time"

	"github.com/gorilla/websocket"
)

var upgrader = websocket.Upgrader{
	ReadBufferSize:  1024,
	WriteBufferSize: 1024,
}

const (
	// Time allowed to write a message to the peer.
	writeWait = 5 * time.Second

	// Maximum message size allowed from peer.
	maxMessageSize = 8192

	// Time allowed to read the next pong message from the peer.
	pongWait = 30 * time.Second

	// Send pings to peer with this period. Must be less than pongWait.
	pingPeriod = (pongWait * 9) / 10

	// Time to wait before force close on connection.
	closeGracePeriod = 5 * time.Second
)

type Client struct {
	conn *websocket.Conn
}

type Session struct {
	registered_client *Client
}

func (session *Session) send(message interface{}) error {
	return session.registered_client.conn.WriteJSON(message)
}

func (session *Session) receive(command interface{}) (interface{}, error) {
	err := session.registered_client.conn.ReadJSON(command)
	return command, err
}

type Dispatcher func(*Session, interface{})
type CommandFactory func() interface{}

func (s *Session) Close() {
	s.registered_client.conn.Close()
}
func (s *Session) stream_ws(dispatcher Dispatcher, command_factory CommandFactory) {
	defer s.Close()

	for {
		message, err := s.receive(command_factory())
		if err != nil {
			break
		}
		dispatcher(s, message)
	}
}

func configure_connection(ws *websocket.Conn) {
	ws.SetReadLimit(maxMessageSize)
	ws.SetReadDeadline(time.Now().Add(pongWait))
}

func (session *Session) register_new_client(ws *websocket.Conn) {
	if session.registered_client != nil {
		old_client := session.registered_client
		new_client := Client{ws}
		session.registered_client = &new_client
		old_client.conn.Close()
	}
}

func (session *Session) Open_Web_Socket(w http.ResponseWriter, r *http.Request, dispatcher Dispatcher, command_factory CommandFactory) {
	ws, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		configure_connection(ws)
		session.register_new_client(ws)
		session.stream_ws(dispatcher, command_factory)
	} else {
		log.Fatalf("Error upgrading connection for websocket use: %s", err.Error())
	}
}
