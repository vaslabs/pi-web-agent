import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OnlineIndicatorComponent } from './online-indicator.component';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';


@NgModule({
  declarations: [OnlineIndicatorComponent],
  imports: [
    CommonModule,
    MatIconModule,
    MatProgressSpinnerModule,
  ],
  exports: [
    OnlineIndicatorComponent
  ]
})
export class OnlineIndicatorModule { }
