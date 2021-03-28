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
    this.websocketService.connect();
  }

  commandSink(): Subject<any> | null {
    return this.websocketService.subject;
  }

  eventSource(): BehaviorSubject<any> {
    return this.messageSource;
  }

  sendCommand(command: PiCommand): void {
    this.commandSink()?.next(command);
  }

  commandEventStream(): Observable<any> | null {
    const commandSink = this.commandSink();
    if (commandSink) {
      const observable = new Observable(
        (observer: Observer<any>) => {
          observer.next = event => {
            this.zone.run(() => {
              this.sendCommand(event);
            });
          };

          observer.error = error => {
            this.zone.run( () => {
              observer.error(error);
            });
          };
          commandSink?.subscribe(observer);
        }
      );
      return observable;
    } else {
      return null;
    }
  }
}

export interface PiCommand {
  Action_Type: string;
}
