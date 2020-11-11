import {Component, Input, OnInit} from '@angular/core';
import {BackendService} from '../../backend.service';

@Component({
  selector: 'app-cal-split-flap',
  templateUrl: './cal-split-flap.component.html',
  styleUrls: ['./cal-split-flap.component.css']
})
export class CalSplitFlapComponent implements OnInit {

  @Input()
  type = 'None';
  status;
  statusArray;

  constructor(private backend: BackendService) { }

  ngOnInit(): void {
    this.backend.getStatus(this.type).subscribe(json =>
    {
      this.status = json;
      this.statusArray = [];
      for (let key in json){
        this.statusArray.push({description: key, value: json[key]});
      }
      console.log(this.status);
    });
  }

  setParameter(parameter, value): void {
    this.backend.setParameter(this.type, parameter, value).subscribe(ans =>
    {
      console.log(ans);
    });
  }
}
