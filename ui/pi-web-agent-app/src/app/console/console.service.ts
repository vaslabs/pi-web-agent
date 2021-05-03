import { PiControlService } from './../pi-control.service';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { distinctUntilChanged, filter, map } from 'rxjs/operators';

export interface IConsoleMessage {
  Console_Message: string;
}

@Injectable({
  providedIn: 'root'
})
export class ConsoleService {
  constructor(private piControl: PiControlService) {}

  getConsoleStream(): Observable<string> {
    return this.piControl.eventSource().pipe(
      filter(
        (consoleMessage: IConsoleMessage) => !!consoleMessage.Console_Message
      ),
      map(consoleMessage => consoleMessage.Console_Message),
      distinctUntilChanged()
    );
  }
}
