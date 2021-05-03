import { ConsoleService } from './../console/console.service';
import {
  PackageUpdate,
  UpdateManagementService
} from './update-management.service';
import { ChangeDetectionStrategy, Component, OnInit } from '@angular/core';
import { merge, Observable, Subject } from 'rxjs';
import { filter } from 'rxjs/operators';
import { PiControlService } from '../pi-control.service';

@Component({
  selector: 'app-update-management',
  templateUrl: './update-management.component.html',
  styleUrls: ['./update-management.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class UpdateManagementComponent implements OnInit {
  packageUpdates$: Observable<Array<PackageUpdate>>;
  console$: Observable<string>;
  constructor(
    private updateManagementService: UpdateManagementService,
    private consoleService: ConsoleService
  ) {
    this.packageUpdates$ = this.updateManagementService.getPackageUpdateStream();
    this.console$ = this.consoleService.getConsoleStream();
  }

  ngOnInit(): void {
    this.updateManagementService.initialize();
  }

  updateSystem(event: Event): void {
    event.stopPropagation();
    this.updateManagementService.applyUpdates();
  }
}
