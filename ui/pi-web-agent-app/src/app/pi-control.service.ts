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
    this.websocketService.connect((next: any) => this.messageSource.next(next));
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
}

export interface PiCommand {
  Action_Type: string;
}
