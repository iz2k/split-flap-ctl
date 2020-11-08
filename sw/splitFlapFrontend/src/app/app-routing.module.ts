import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {ClockComponent} from './clock/clock.component';
import {WeatherComponent} from './weather/weather.component';
import {DashboardComponent} from './dashboard/dashboard.component';


const routes: Routes = [
  { path: '', component: DashboardComponent },
  { path: 'clock', component: ClockComponent },
  { path: 'weather', component: WeatherComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
