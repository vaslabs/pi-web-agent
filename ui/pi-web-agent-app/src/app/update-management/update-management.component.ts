import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { PiControlService } from '../pi-control.service';

@Component({
  selector: 'app-update-management',
  templateUrl: './update-management.component.html',
  styleUrls: ['./update-management.component.scss']
})
export class UpdateManagementComponent implements OnInit {

  constructor(private piControl: PiControlService) { }

  packageUpdates: PackageUpdate[] = [];

  ngOnInit(): void {
    this.piControl.sendCommand({Action_Type: 'AVAILABLE_UPDATES'});

    this.piControl.eventSource().subscribe(
      (packageUpdates: PackageUpdate[]) =>
        this.packageUpdates = packageUpdates
    );
  }


}

interface PackageUpdate {
  Name: string;
  Current_Version: string;
  Next_Version: string;
}
