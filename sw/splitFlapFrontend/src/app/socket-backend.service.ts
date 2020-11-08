import { Injectable } from '@angular/core';
import {Socket} from 'ngx-socket-io';

@Injectable({
  providedIn: 'root'
})
export class SocketBackendService extends Socket {

  constructor() {
        super({ url: 'http://localhost:8081', options: {} });
        console.log('Creating Backend WebSocket Service');
        this.ioSocket.on('connect', () => console.log('Backend WebSocket Connected'));
  }
}
