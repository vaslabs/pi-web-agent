import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class SystemInfoService {

  private api_endpoint = "/api/info"

  constructor(private http: HttpClient) { }


  fetch_system_info() {
    return this.http.get<SystemInfo>(`${this.api_endpoint}/os_info`)
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
