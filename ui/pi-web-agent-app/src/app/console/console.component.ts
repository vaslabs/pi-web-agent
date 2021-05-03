import { AfterViewInit, Component, OnInit, ViewChild } from '@angular/core';
import { NgTerminal } from 'ng-terminal';
import { Subject } from 'rxjs';
import { PiControlService } from '../pi-control.service';
import { Terminal } from 'xterm';

@Component({
  selector: 'app-console',
  templateUrl: './console.component.html',
  styleUrls: ['./console.component.scss']
})
export class ConsoleComponent implements OnInit, AfterViewInit {
  @ViewChild('term', { static: true })
  child!: NgTerminal;

  writeSubject: Subject<string> = new Subject();
  underlying!: Terminal;

  constructor(private piControl: PiControlService) { }

  ngOnInit(): void {
    this.writeSubject.next('$');
    this.piControl.eventSource().subscribe(
      (consoleMessage: ConsoleMessage) => {
        console.log(consoleMessage.Console_Message);
        if (consoleMessage.Console_Message) {
          this.writeSubject.next(consoleMessage.Console_Message + '\r');
        }
      }
    );
  }

  ngAfterViewInit(): void {
    this.underlying = this.child.underlying;
    this.underlying.setOption('fontSize', 20);
    this.underlying.setOption('rendererType', 'dom');
    this.child.write('$ ');
  }

}


interface ConsoleMessage {
  Console_Message: string;
}
