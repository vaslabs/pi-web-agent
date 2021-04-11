package net

import (
	"io"
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
	writeWait = 10 * time.Second

	// Maximum message size allowed from peer.
	maxMessageSize = 8192

	// Time allowed to read the next pong message from the peer.
	pongWait = 60 * time.Second

	// Send pings to peer with this period. Must be less than pongWait.
	pingPeriod = (pongWait * 9) / 10
)

type Client struct {
	conn *websocket.Conn
}

func (client *Client) SendJSON(message interface{}) {
	client.ExtendWriteDeadline()
	err := client.conn.WriteJSON(message)
	if err != nil {
		log.Printf("Error sending message to websocket %s", err)
	}
}

func (client *Client) ExtendWriteDeadline() {
	log.Printf("Extending dealine %s", time.Now().Add(writeWait))
	client.conn.SetWriteDeadline(time.Now().Add(writeWait))
}

type Session struct {
	registered_client *Client
}

type SessionWithoutClient struct{}

func (*SessionWithoutClient) Error() string {
	return "Session without client"
}

func NewSession() Session {
	return Session{nil}
}

func (session *Session) Send(message interface{}) {
	log.Printf("Sending message %s", message)
	session.registered_client.SendJSON(message)
}

func (session *Session) receive() (*io.Reader, error) {
	if session.registered_client != nil {
		_, r, err := session.registered_client.conn.NextReader()
		return &r, err
	} else {
		return nil, &SessionWithoutClient{}
	}
}

type Dispatcher func(session *Session, nextCommand *io.Reader)

func (s *Session) Close() {
	s.registered_client.conn.Close()
}
func (s *Session) stream_ws(dispatcher Dispatcher) {
	defer s.Close()
	for {
		encapsulated_message, err := s.receive()
		if err != nil {
			log.Printf("Closing websocket connection due to %s", err.Error())
			break
		}
		dispatcher(s, encapsulated_message)
	}
}

func ping_writer(ws *websocket.Conn) {
	pingTicker := time.NewTicker(pingPeriod)
	defer func() {
		pingTicker.Stop()
		ws.Close()
	}()
	for {
		<-pingTicker.C
		ws.SetWriteDeadline(time.Now().Add(writeWait))
		if err := ws.WriteMessage(websocket.PingMessage, []byte{}); err != nil {
			return
		}
		log.Printf("Sending ping message...")
	}
}

func configure_connection(ws *websocket.Conn) {
	go ping_writer(ws)
	ws.SetReadLimit(maxMessageSize)
	ws.SetReadDeadline(time.Now().Add(pongWait))
	ws.SetPongHandler(func(string) error {
		log.Print("Pong Received")
		ws.SetReadDeadline(time.Now().Add(pongWait))
		return nil
	})
}

func (session *Session) register_new_client(ws *websocket.Conn) {
	if session.registered_client != nil {
		old_client := session.registered_client
		new_client := Client{ws}
		session.registered_client = &new_client
		old_client.conn.Close()
	} else {
		session.registered_client = &Client{ws}
	}
}

func (session *Session) Open_Web_Socket(w http.ResponseWriter, r *http.Request, dispatcher Dispatcher) {
	//TODO find a way to safeguard this a bit
	upgrader.CheckOrigin = func(r *http.Request) bool {
		return true
	}
	ws, err := upgrader.Upgrade(w, r, nil)

	log.Print("Connecting to websocket")
	if err == nil {
		configure_connection(ws)
		session.register_new_client(ws)
		session.stream_ws(dispatcher)
	} else {
		log.Printf("Error upgrading connection for websocket use: %s", err.Error())
	}
}
