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
import {BackendService} from './backend.service';
import {HttpClientModule} from '@angular/common/http';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatDatepickerModule} from '@angular/material/datepicker';
import {ReactiveFormsModule} from '@angular/forms';
import {MatInputModule } from '@angular/material/input';
import {JSBAngularFlipClockModule} from 'jsb-angular-flip-clock';
import {MatNativeDateModule} from "@angular/material/core";


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
    JSBAngularFlipClockModule,
    NgbModule,
    SocketIoModule,
    HttpClientModule,
    MatFormFieldModule,
    MatInputModule,
    MatDatepickerModule,
    MatNativeDateModule,
    ReactiveFormsModule
  ],
  providers: [BackendService],
  bootstrap: [AppComponent]
})
export class AppModule { }
