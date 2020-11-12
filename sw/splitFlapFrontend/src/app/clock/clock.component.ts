import {BackendService} from '../backend.service';
import {Component, OnInit} from '@angular/core';
import {FormControl, FormGroup} from "@angular/forms";

@Component({
  selector: 'app-clock',
  templateUrl: './clock.component.html',
  styleUrls: ['./clock.component.css']
})

export class ClockComponent implements OnInit {

  clockTime: any;
  HoursTensPlace = 0;
  HoursOnesPlace = 0;
  MinutesTensPlace = 0;
  MinutesOnesPlace = 0;
  SecondsTensPlace = 0;
  SecondsOnesPlace = 0;

  date: FormControl;
  tzFormGroup: FormGroup;
  timezone = new FormControl('');

  calibrationMode = false;

  constructor(private backend: BackendService) { }


  ngOnInit(): void {
    this.backend.getTime().subscribe(json => {
      this.updateClockTime(json);
      this.timezone.valueChanges.subscribe(tz => this.timezoneChange(tz));
    });
    this.backend.getMode().subscribe(json => this.updateMode(json));
    this.tzFormGroup = new FormGroup(
      {
                timezone: this.timezone
              });
    this.periodicEvent();
  }

  periodicEvent(): void {
    setInterval
      (_ => {
        this.incrementClockTime();
        if (!this.calibrationMode) {
          this.updateFlipClockWidget();
        }
      }, 1000);
  }

  updateClockTime(json): void {
    console.log(json);
    this.clockTime = json;
    if (this.timezone.value.nameValue !== this.clockTime.timezone) {
      this.timezone.setValue(this.clockTime.timezone);
    }
    this.updateFlipClockWidget();
  }

  updateMode(json): void {
    if (json.mode === 'clock') {
      this.calibrationMode = false;
    }else{
      this.calibrationMode = true;
    }
  }

  updateFlipClockWidget(): void {
      this.date = new FormControl(new Date(this.clockTime.year, this.clockTime.month - 1, this.clockTime.day,
                                          this.clockTime.hour, this.clockTime.minute, this.clockTime.second));
      this.HoursTensPlace = Math.floor(this.clockTime.hour / 10);
      this.HoursOnesPlace = Math.floor(this.clockTime.hour % 10);
      this.MinutesTensPlace = Math.floor(this.clockTime.minute / 10);
      this.MinutesOnesPlace = Math.floor(this.clockTime.minute % 10);
      this.SecondsTensPlace = Math.floor(this.clockTime.second / 10);
      this.SecondsOnesPlace = Math.floor(this.clockTime.second % 10);
  }

  incrementClockTime(): void {
    this.clockTime.second++;
    if (this.clockTime.second > 59) {
      this.clockTime.second = 0;
      this.clockTime.minute++;
      if (this.clockTime.minute > 59){
        this.clockTime.minute = 0;
        this.clockTime.hour++;
        if (this.clockTime.hour > 23){
          this.clockTime.hour = 0;
        }
      }
    }
  }

  applyCalibrationMode(calibrationMode): void {
    if (calibrationMode) {
      this.backend.setMode('calibration').subscribe(json => {this.updateMode(json); });
    }else {
      this.backend.setMode('clock').subscribe(json => {this.updateMode(json); });
    }
  }

  timezoneChange(tz): void {
    console.log('timezone changed');
    console.log(tz);
    this.backend.setTimeZone(tz).subscribe(ans => {
      this.backend.getTime().subscribe(json => this.updateClockTime(json));
      console.log(ans);
    });
  }

}
