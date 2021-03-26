import { Injectable } from '@angular/core';
import { Observable, Subject, Observer, BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class WebsocketService {
  subject: Subject<MessageEvent> = null;
  defaultMessage: any = {}

  ready = new BehaviorSubject(this.defaultMessage)

  constructor() { }

  private url = "/api/control/stream"

  public connect(): Subject<MessageEvent> {
    if (!this.subject) {
      this.subject = this.create();
      console.log("Successfully connected: ");
    }
    this.ready.next({ready:true})
    return this.subject;
  }

  private create(): Subject<MessageEvent> {
    let ws = new WebSocket(this.url);

    let observable = Observable.create((obs: Observer<MessageEvent>) => {
      ws.onmessage = obs.next.bind(obs);
      ws.onerror = obs.error.bind(obs);
      ws.onclose = obs.complete.bind(obs);
      return ws.close.bind(ws);
    });
    let observer = {
      next: (data: Object) => {
        if (ws.readyState === WebSocket.OPEN) {
          ws.send(JSON.stringify(data));
        }
      }
    };
    return Subject.create(observer, observable);
  }
}