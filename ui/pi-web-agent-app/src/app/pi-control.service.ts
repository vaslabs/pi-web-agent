import { NgZone, OnDestroy } from '@angular/core';
import { Injectable } from '@angular/core';
import { Observable, BehaviorSubject,  Subscription } from 'rxjs';
import { WebsocketService, ConnectionStatus} from './websocket.service';
@Injectable({
  providedIn: 'root'
})
export class PiControlService implements OnDestroy {

  defaultMessage: any = {};
  private messageSource$ = new BehaviorSubject(this.defaultMessage);
  private webSocketSubscription: Subscription| null = null;
  currentMessage$: Observable<any> = this.messageSource$.asObservable();

  constructor(
    private zone: NgZone,
    private websocketService: WebsocketService
  ) {
    const broker = (next: any) => this.messageSource$.next(next);
    this.connectToSocket(broker);
  }

  private connectToSocket(broker: (next: any) => void): void {
    this.webSocketSubscription = this.websocketService.getMessageStream().subscribe(
      broker
    );
  }


  eventSource(): Observable<any> {
    return this.currentMessage$;
  }

  sendCommand(command: PiCommand): void {
    this.websocketService.sendMessage(command);
  }

  getConnectionStatus(): Observable<ConnectionStatus>{
    return this.websocketService.getConnectionStatus();
  }

  ngOnDestroy(): void{
    if (this.webSocketSubscription !== null){
      this.webSocketSubscription.unsubscribe();
    }
  }

}

export interface PiCommand {
  Action_Type: string;
}
