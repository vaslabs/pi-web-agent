import { Component, OnInit } from '@angular/core';
import { PiControlService } from '../pi-control.service';

@Component({
  selector: 'app-poweroff',
  templateUrl: './poweroff.component.html',
  styleUrls: ['./poweroff.component.scss']
})
export class PoweroffComponent implements OnInit {

  constructor(private piControlService: PiControlService) { }

  ngOnInit(): void {
  }

  poweroff(): void {
    this.piControlService.sendCommand({Action_Type: 'POWER_OFF'});
  }

  reboot(): void {
    this.piControlService.sendCommand({Action_Type: 'REBOOT'});
  }

}
