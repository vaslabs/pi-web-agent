import { Injectable } from '@angular/core';
import { Observable, Subject, Observer, BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class WebsocketService {
  subject: Subject<any> | null = null;
  defaultMessage: any = {};

  ready = new BehaviorSubject(this.defaultMessage);

  constructor() {
  }

  private url(): string {
    const protocol = window.location.protocol.replace('http', 'ws');
    const host = window.location.host;
    return `${protocol}//${host}/api/control/stream`;
  }
  public connect(): void{
    try {
      if (!this.subject) {
        console.log(`Connecting to ${this.url()} for the first time`);
        this.subject = this.create();
        console.log('Successfully connected: ');
      }
      this.ready.next({ready: true});
    } catch (error) {
      console.log(`Failed to connect due to ${error}`);
    }
  }

  private create(): Subject<any> {
    const ws = new WebSocket(this.url());

    const observable = Observable.create((obs: Observer<any>) => {
      ws.onmessage = obs.next.bind(obs);
      ws.onerror = obs.error.bind(obs);
      ws.onclose = obs.complete.bind(obs);
      return ws.close.bind(ws);
    });
    const observer = {
      next: (data: any) => {
        if (ws.readyState === WebSocket.OPEN) {
          console.log(`Forwarding ${JSON.stringify(data)} to websocket`);
          ws.send(JSON.stringify(data));
        } else {
          console.log(`Websocket is not open but ${ws.readyState}`);
        }
      }
    };
    return Subject.create(observer, observable);
  }
}
