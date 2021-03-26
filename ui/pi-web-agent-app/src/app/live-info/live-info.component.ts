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
    this.system_info_service.fetch_system_info().subscribe(
      (info: SystemInfo) => this.system_info = info
    );
  }

}