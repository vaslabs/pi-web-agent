import { Component, OnInit } from '@angular/core';
import { SystemInfo, SystemInfoService } from '../system-info.service';

@Component({
  selector: 'app-live-info',
  templateUrl: './live-info.component.html',
  styleUrls: ['./live-info.component.scss']
})
export class LiveInfoComponent implements OnInit {

  constructor(private systemInfoService: SystemInfoService) { }

  systemInfo: SystemInfo = {
    Temperature: '',
    Kernel: '',
    OS_Info: {
      Id: '',
      Version_Codename: ''
    }
  };
  ngOnInit(): void {
    this.periodic_update(this.systemInfoService);
  }

  private periodic_update(infoService: SystemInfoService): void {
    console.log('Sending command for display live info');
    infoService.fetchSystemInfo();
    setTimeout(() => this.periodic_update(infoService), 10000);
  }

}
