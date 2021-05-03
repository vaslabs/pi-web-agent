import { Injectable } from '@angular/core';
import { merge, Subject } from 'rxjs';
import { Observable } from 'rxjs/internal/Observable';
import { filter } from 'rxjs/operators';
import { PiControlService } from '../pi-control.service';

export interface PackageUpdate {
  Name: string;
  Current_Version: string;
  Next_Version: string;
}

@Injectable({
  providedIn: 'root'
})
export class UpdateManagementService {
  private readonly packageUpdatesResetValue: Array<PackageUpdate> = [];
  packageUpdatesReset$ = new Subject<Array<PackageUpdate>>();
  constructor(private piControl: PiControlService) {}

  getPackageUpdateStream(): Observable<Array<PackageUpdate>> {
    return merge(
      this.piControl
        .eventSource()
        .pipe(
          filter((packageUpdates: Array<PackageUpdate>) =>
            Array.isArray(packageUpdates)
          )
        ),
      this.packageUpdatesReset$
    );
  }
  private resetPackageUpdates(): void {
    this.packageUpdatesReset$.next(this.packageUpdatesResetValue);
  }
  initialize(): void {
    this.piControl.sendCommand({ Action_Type: 'AVAILABLE_UPDATES' });
  }
  applyUpdates(): void {
    this.resetPackageUpdates();
    this.piControl.sendCommand({ Action_Type: 'APPLY_UPDATES' });
  }
}
