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
  underlying!: Terminal;

  writeSubject: Subject<string> = new Subject();

  constructor(private piControl: PiControlService) { }

  ngOnInit(): void {
    this.writeSubject.next('$');
    this.piControl.eventSource().subscribe(
      (consoleMessage: ConsoleMessage) => {
        console.log(consoleMessage.Console_Message);
        if (consoleMessage.Console_Message) {
          this.child.write(consoleMessage.Console_Message + '\r');
        }
      }
    );
  }

  ngAfterViewInit(): void {
    this.underlying = this.child.underlying;
    this.underlying.setOption('fontSize', 20);
    this.child.write('$ ');
  }

}


interface ConsoleMessage {
  Console_Message: string;
}
