import { Injectable } from '@angular/core';
import { Observable, Subject, Observer } from 'rxjs';
import { webSocket } from 'rxjs/webSocket';

@Injectable({
  providedIn: 'root'
})
export class WebsocketService {
  subject: Subject<any> | null = null;

  constructor() {
  }

  private url(): string {
    const protocol = window.location.protocol.replace('http', 'ws');
    const host = window.location.host;
    return `${protocol}//${host}/api/control/stream`;
  }
  public connect(subscriber: (next: any) => void): void  {
    try {
      if (!this.subject) {
        console.log(`Connecting to ${this.url()} for the first time`);
        this.subject = this.create();
        this.subject.subscribe(subscriber);
        console.log('Successfully connected: ');
      }
    } catch (error) {
      console.log(`Failed to connect due to ${error}`);
    }
  }

  sendMessage(event: any): void {
    this.subject?.next(event);
  }

  private create(): Subject<any> {
    return webSocket(this.url());
  }
}
