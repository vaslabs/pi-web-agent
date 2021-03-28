import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { PiControlService } from './pi-control.service';

@Injectable({
  providedIn: 'root'
})
export class SystemInfoService {

  constructor(private piControlService: PiControlService) { 
    
  }


  fetchSystemInfo() {
    this.piControlService.sendCommand({Action_Type: "DISPLAY_LIVE_INFO"})
  }
}

export interface SystemInfo {
  Temperature: string,
  Kernel: string,
  OS_Info: {
    Id: string,
    Version_Codename: string
  }
}
