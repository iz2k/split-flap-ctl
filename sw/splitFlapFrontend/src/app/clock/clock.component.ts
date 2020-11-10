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

  constructor(private backend: BackendService) { }


  ngOnInit(): void {
    this.backend.getTime().subscribe(json => this.updateClockTime(json));
    this.tzFormGroup = new FormGroup({
    timezone: this.timezone
  });
  }

  updateClockTime(json): void {
    this.clockTime = json;
    this.timezone.setValue(this.clockTime.timezone);
    this.updateFlipClockWidget();
    setInterval
      (_ => {
        this.incrementClockTime();
        this.updateFlipClockWidget();
      }, 1000);
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

}
