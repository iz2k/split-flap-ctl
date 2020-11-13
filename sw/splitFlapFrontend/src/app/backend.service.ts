import { Injectable } from '@angular/core';
import {Socket} from 'ngx-socket-io';
import {Observable} from 'rxjs';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {backendHost, backendPort} from '../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class BackendService extends Socket {

  private urlEndPoint = 'http://' + backendHost + ':' + backendPort;

  constructor(private http: HttpClient){
        super({ url: 'http://' + backendHost + ':' + backendPort, options: {} });
        console.log('Creating Backend Service');
        this.ioSocket.on('connect', () => console.log('Backend WebSocket Connected'));
  }

  getTime(): Observable<any> {
    return this.http.get<any>(this.urlEndPoint + '/get-time');
  }

  getStatus(type): Observable<any> {
    return this.http.get<any>(this.urlEndPoint + '/get-status?type=' + type);
  }

  getMode(): Observable<any> {
    return this.http.get<any>(this.urlEndPoint + '/get-mode');
  }

  setMode(value): Observable<any> {
    return this.http.get<any>(this.urlEndPoint + '/set-mode?mode=' + value);
  }

  setParameter(type, parameter, value): Observable<any> {
    return this.http.get<any>(this.urlEndPoint + '/set-parameter?type=' + type + '&parameter=' + parameter + '&value=' + value);
  }

  setTimeZone(timezone): Observable<any> {
    return this.http.post<any>(this.urlEndPoint + '/set-timezone', timezone,
      {
        headers: new HttpHeaders({
          'Content-Type':  'application/json',
        })
      });
  }

  getGeocodeApi(): Observable<any> {
    return this.http.get<any>(this.urlEndPoint + '/get-geocodeapi');
  }
}
