import { Injectable, OnDestroy } from '@angular/core';
import { retryBackoff } from 'backoff-rxjs';
import { Observable, Subject, Observer, Subscription } from 'rxjs';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';
import { share } from 'rxjs/operators';

@Injectable({
  providedIn: 'root',
})
export class WebsocketService {
  private websocket: WebSocketSubject<any>;
  private messageStream: Observable<any>;
  constructor() {
    this.websocket = this.create();
    this.messageStream = this.websocket.pipe(retryBackoff(1000), share());
  }

  private url(): string {
    const protocol = window.location.protocol.replace('http', 'ws');
    const host = window.location.host;
    return `${protocol}//${host}/api/control/stream`;
  }
  public getMessageStream(): Observable<any>{
    return this.messageStream;
  }

  sendMessage(event: any): void {
    this.websocket?.next(event);
  }

  private create(): WebSocketSubject<any>{
    return webSocket(this.url());
  }
}
