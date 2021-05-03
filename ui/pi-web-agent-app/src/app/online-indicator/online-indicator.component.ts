import { ConnectionStatus } from './../websocket.service';
import { Observable } from 'rxjs';
import { PiControlService } from './../pi-control.service';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-online-indicator',
  templateUrl: './online-indicator.component.html',
  styleUrls: ['./online-indicator.component.scss']
})
export class OnlineIndicatorComponent implements OnInit {
  connectionStatus$: Observable<ConnectionStatus>;
  ConnectionStatus = ConnectionStatus;
  constructor(private controlService: PiControlService) {
    this.connectionStatus$ = this.controlService.getConnectionStatus();
  }

  ngOnInit(): void {
  }

}
