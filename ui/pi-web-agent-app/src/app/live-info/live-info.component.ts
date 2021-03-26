import { Component, OnInit } from '@angular/core';
import { SystemInfo, SystemInfoService } from '../system-info.service';

@Component({
  selector: 'app-live-info',
  templateUrl: './live-info.component.html',
  styleUrls: ['./live-info.component.scss']
})
export class LiveInfoComponent implements OnInit {

  constructor(private system_info_service: SystemInfoService) { }

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
  }

  private periodic_update(infoService: SystemInfoService): void {
    
    infoService.fetch_system_info().subscribe(
      (info: SystemInfo) => this.system_info = info
    );
    setTimeout(() => this.periodic_update(infoService), 10000);
  }

}