import {
  AfterViewInit,
  ChangeDetectionStrategy,
  Component,
  Input,
  OnInit,
  ViewChild
} from '@angular/core';
import { NgTerminal } from 'ng-terminal';
import { Subject } from 'rxjs';
import { PiControlService } from '../pi-control.service';
import { Terminal } from 'xterm';

@Component({
  selector: 'app-console',
  templateUrl: './console.component.html',
  styleUrls: ['./console.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class ConsoleComponent implements OnInit, AfterViewInit {
  @ViewChild('term', { static: true })
  child!: NgTerminal;
  underlying!: Terminal;
  source$ = new Subject<string>();
  @Input() fontSize = 16;

  @Input() set source(state: string | null) {
    if (this.underlying && state !== null) {
      console.log(state);
      this.source$.next(`${state}\r\n`);
    }
  }

  constructor(private piControl: PiControlService) {}

  ngOnInit(): void {}

  ngAfterViewInit(): void {
    this.underlying = this.child.underlying;
    this.underlying.setOption('fontSize', this.fontSize);
  }
}
