import { Component, OnInit } from '@angular/core';
import {FormControl} from '@angular/forms';
import {BackendService} from '../backend.service';
import {GeocodeService} from './geocode.service';

import Map from 'ol/Map';
import View from 'ol/View';
import OSM from 'ol/source/OSM';
import * as olProj from 'ol/proj';
import TileLayer from 'ol/layer/Tile';

@Component({
  selector: 'app-weather',
  templateUrl: './weather.component.html',
  styleUrls: ['./weather.component.css']
})
export class WeatherComponent implements OnInit {

  date = new FormControl(new Date());
  cityName: any;
  geocodeResult: any;
  location: any;
  map: any;
  private zoom: number;

  constructor(private backend: BackendService, private geocode: GeocodeService) { }

  ngOnInit(): void {
    this.backend.getGeocodeApi().subscribe(json => {
      this.geocode.setApi(json.api);
      console.log('Geocode API retrieved');
    });
    this.map = new Map({
      controls: [],
      target: 'cityMap',
      layers: [
        new TileLayer({
          source: new OSM()
        })
      ],
      view: new View({
        center: olProj.fromLonLat([0, 0]),
        zoom: 1
      })
    });
  }

  searchCity(): void {
    this.geocode.getCityGeocode(this.cityName).subscribe(json => {
      this.geocodeResult = json;
      console.log('Geocode result:');
      console.log(this.geocodeResult);
      if (this.geocodeResult.features[0] !== undefined)
      {
        this.location = this.geocodeResult.features[0];
        this.map.setView(new View({
          center: olProj.fromLonLat(this.location.geometry.coordinates),
          zoom: 13
        }));
      }else
      {
        this.location = undefined;
        this.map.setView(new View({
          center: olProj.fromLonLat([0, 0]),
          zoom: 1
        }));
      }
      console.log(this.location);
    });
  }

}
