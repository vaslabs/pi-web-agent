import { Injectable } from '@angular/core';
import { retryBackoff } from 'backoff-rxjs';
import { BehaviorSubject, Observable, throwError } from 'rxjs';
import { catchError,  distinctUntilChanged,  finalize, share, tap } from 'rxjs/operators';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';

export enum ConnectionStatus{
  connected = 'connected',
  connecting = 'connecting',
  disconnected = 'disconnected',
}
@Injectable({
  providedIn: 'root',
})
export class WebsocketService {
  private websocket$: WebSocketSubject<any>;
  private messageStream$: Observable<any>;
  private connectionStatus$ = new BehaviorSubject<ConnectionStatus>(ConnectionStatus.connecting);
  constructor() {
    this.websocket$ = this.create();
    this.messageStream$ = this.websocket$.pipe(
      catchError((error: Error) => {
        this.connectionStatus$.next(ConnectionStatus.connecting);
        return throwError(error);
      }),
      retryBackoff(1000),
      tap(() => {
         this.connectionStatus$.next(ConnectionStatus.connected);
      }),
      finalize(() => this.connectionStatus$.next(ConnectionStatus.disconnected)),
      share()
    );
  }

  private url(): string {
    const protocol = window.location.protocol.replace('http', 'ws');
    const host = window.location.host;
    return `${protocol}//${host}/api/control/stream`;
  }
  public getMessageStream(): Observable<any>{
    return this.messageStream$;
  }

  public getConnectionStatus(): Observable<ConnectionStatus>{
    return this.connectionStatus$.pipe(
      distinctUntilChanged()
    );
  }

  sendMessage(event: any): void {
    this.websocket$?.next(event);
  }

  private create(): WebSocketSubject<any>{
    return webSocket(this.url());
  }
}
