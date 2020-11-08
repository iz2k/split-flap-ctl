import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { AppRoutingModule } from './app-routing.module';
import { ClockComponent } from './clock/clock.component';
import { HeaderComponent } from './header/header.component';
import { FooterComponent } from './footer/footer.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { WeatherComponent } from './weather/weather.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import {SocketIoModule} from 'ngx-socket-io';
import {SocketBackendService} from "./socket-backend.service";

@NgModule({
  declarations: [
    AppComponent,
    ClockComponent,
    HeaderComponent,
    FooterComponent,
    WeatherComponent,
    DashboardComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    NgbModule,
    SocketIoModule
  ],
  providers: [SocketBackendService],
  bootstrap: [AppComponent]
})
export class AppModule { }
