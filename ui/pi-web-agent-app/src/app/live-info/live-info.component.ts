import { Component, OnDestroy, OnInit } from '@angular/core';
import { interval, Subscription, Observable } from 'rxjs';
import { filter, map, startWith, tap } from 'rxjs/operators';
import { PiControlService } from '../pi-control.service';
import { SystemInfo, SystemInfoService } from '../system-info.service';

@Component({
  selector: 'app-live-info',
  templateUrl: './live-info.component.html',
  styleUrls: ['./live-info.component.scss']
})
export class LiveInfoComponent implements OnInit, OnDestroy {
  public systemInfo$: Observable<SystemInfo>;
  private periodicUpdateSubscription: Subscription | null = null;
  private initialState: SystemInfo = {
    Temperature: '',
    Kernel: '',
    OS_Info: {
      Id: '',
      Version_Codename: ''
    }
  }

  constructor(private systemInfoService: SystemInfoService, private piControl: PiControlService) {
    this.systemInfo$ = this.piControl.eventSource().pipe(
      filter(({OS_Info}) => !!OS_Info),
      startWith(this.initialState)
    );
  }

  ngOnInit(): void {
    this.periodicUpdateSubscription = this.periodicUpdate().subscribe();
  }

  ngOnDestroy(): void {
    if (this.periodicUpdateSubscription !== null) {
      this.periodicUpdateSubscription.unsubscribe();
    }
  }

  private periodicUpdate(): Observable<number> {
    return interval(1000).pipe(
      tap(() => this.systemInfoService.fetchSystemInfo())
    );
  }

}
