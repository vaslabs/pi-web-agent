import { Component, OnInit } from '@angular/core';
import { PiControlService } from '../pi-control.service';
import { SystemInfo, SystemInfoService } from '../system-info.service';

@Component({
  selector: 'app-live-info',
  templateUrl: './live-info.component.html',
  styleUrls: ['./live-info.component.scss']
})
export class LiveInfoComponent implements OnInit {

  constructor(private system_info_service: SystemInfoService, private pi_control: PiControlService) { }

  system_info: SystemInfo = {
    Temperature: "",
    Kernel: "",
    OS_Info: {
      Id: "",
      Version_Codename: ""
    }
  }
  ngOnInit(): void {
    this.periodic_update(this.system_info_service)
    this.pi_control.eventSource()?.subscribe(
      (next: any) => {
        console.log("Received " + JSON.stringify(next))
        if (next["OS_Info"]) {
          this.system_info.OS_Info = next.OS_Info
          this.system_info.Kernel = next.Kernel
        }
      }
    )
  }

  private periodic_update(infoService: SystemInfoService): void {
    console.log("Sending command for display live info")
    infoService.fetch_system_info();
    setTimeout(() => this.periodic_update(infoService), 1000);
  }

}