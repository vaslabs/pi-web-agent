import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LiveInfoComponent } from './live-info/live-info.component';
import { PoweroffComponent } from './poweroff/poweroff.component';

const routes: Routes = [
  { path: '', component: LiveInfoComponent },
  { path: 'power-management', component: PoweroffComponent },
];
@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {

 }
