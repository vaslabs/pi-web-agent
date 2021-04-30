import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LiveInfoComponent } from './live-info/live-info.component';
import { PoweroffComponent } from './poweroff/poweroff.component';
import { UpdateManagementComponent } from './update-management/update-management.component';

const routes: Routes = [
  { path: '', component: LiveInfoComponent },
  { path: 'power-management', component: PoweroffComponent },
  { path: 'updates', component: UpdateManagementComponent}
];
@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {

 }
