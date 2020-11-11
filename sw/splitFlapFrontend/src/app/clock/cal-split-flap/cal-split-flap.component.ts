import {Component, Input, OnInit} from '@angular/core';

@Component({
  selector: 'app-cal-split-flap',
  templateUrl: './cal-split-flap.component.html',
  styleUrls: ['./cal-split-flap.component.css']
})
export class CalSplitFlapComponent implements OnInit {

  @Input()
  type = 'None';

  constructor() { }

  ngOnInit(): void {
  }

}
