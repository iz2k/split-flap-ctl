import { Component, OnInit } from '@angular/core';
import {SocketBackendService} from '../socket-backend.service';

@Component({
  selector: 'app-footer',
  templateUrl: './footer.component.html',
  styleUrls: ['./footer.component.css']
})
export class FooterComponent implements OnInit {

  constructor(private backend: SocketBackendService) { }

  osInfo;

  ngOnInit(): void {
        this.backend.ioSocket.on('osInfo', json => this.onOsInfo(json));
  }

  onOsInfo(json): void {
    this.osInfo = JSON.parse(json);
    console.log(this.osInfo);
  }

}
