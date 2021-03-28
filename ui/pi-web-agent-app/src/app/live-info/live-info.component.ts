import { Component, OnInit } from '@angular/core';
import { PiControlService } from '../pi-control.service';
import { SystemInfo, SystemInfoService } from '../system-info.service';

@Component({
  selector: 'app-live-info',
  templateUrl: './live-info.component.html',
  styleUrls: ['./live-info.component.scss']
})
export class LiveInfoComponent implements OnInit {

  constructor(private systemInfoService: SystemInfoService, private piControl: PiControlService) { }

  systemInfo: SystemInfo = {
    Temperature: "",
    Kernel: "",
    OS_Info: {
      Id: "",
      Version_Codename: ""
    }
  }
  ngOnInit(): void {
    this.periodicUpdate(this.systemInfoService)
    this.piControl.eventSource()?.subscribe(
      (next: any) => {
        console.log("Received " + JSON.stringify(next))
        if (next["OS_Info"]) {
          this.systemInfo.OS_Info = next.OS_Info
          this.systemInfo.Kernel = next.Kernel
          this.systemInfo.Temperature = next.Temperature
        }
      }
    )
  }

  private periodicUpdate(infoService: SystemInfoService): void {
    console.log("Sending command for display live info")
    infoService.fetchSystemInfo();
    setTimeout(() => this.periodicUpdate(infoService), 1000);
  }

}