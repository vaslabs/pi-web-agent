import { NgZone } from '@angular/core';
import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';
import { Observable, BehaviorSubject, Observer } from 'rxjs';
import { WebsocketService } from './websocket.service';
@Injectable({
  providedIn: 'root'
})
export class PiControlService {

  defaultMessage: any = {};
  private messageSource = new BehaviorSubject(this.defaultMessage);
  currentMessage: Observable<any> = this.messageSource.asObservable();

  constructor(
    private zone: NgZone,
    private websocketService: WebsocketService
  ) {
    const broker = (next: any) => this.messageSource.next(next);
    this.connectToSocket(broker);
  }

  private connectToSocket(broker: (next: any) => void): void {
    this.websocketService.connect(broker, (error: any) => {
      console.log(`Attempting to reconnect to socket after ${JSON.stringify(error)}`);
      this.connectToSocket(broker);
    });
  }

  commandSink(): Subject<any> | null {
    return this.websocketService.subject;
  }

  eventSource(): Observable<any> {
    return this.currentMessage;
  }

  sendCommand(command: PiCommand): void {
    this.commandSink()?.next(command);
  }

  private ping(): void {
    this.commandSink()?.next('ping');
  }
}

export interface PiCommand {
  Action_Type: string;
}
