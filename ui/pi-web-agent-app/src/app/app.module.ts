import { OnlineIndicatorModule } from './online-indicator/online-indicator.module';
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LiveInfoComponent } from './live-info/live-info.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import {MatDividerModule} from '@angular/material/divider';
import {MatListModule} from '@angular/material/list';
import { HttpClientModule } from '@angular/common/http';
import { PoweroffComponent } from './poweroff/poweroff.component';
import {MatButtonModule} from '@angular/material/button';
import {MatIconModule} from '@angular/material/icon';
import {MatSidenavModule} from '@angular/material/sidenav';
import {MatToolbarModule} from '@angular/material/toolbar';
import { MainViewComponent } from './main-view/main-view.component';
import { UpdateManagementComponent } from './update-management/update-management.component';

@NgModule({
  declarations: [
    AppComponent,
    LiveInfoComponent,
    PoweroffComponent,
    MainViewComponent,
    UpdateManagementComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatDividerModule,
    MatListModule,
    HttpClientModule,
    MatIconModule,
    OnlineIndicatorModule,
    MatSidenavModule,
    MatToolbarModule,
    MatButtonModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
