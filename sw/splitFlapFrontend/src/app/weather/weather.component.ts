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
  geocodeAPI: any;
  geocodeResult: any;
  configCityName: any;
  configGeocodeAPI: any;
  location: any;
  map: any;
  private zoom: number;

  constructor(private backend: BackendService, private geocode: GeocodeService) { }

  ngOnInit(): void {
    this.backend.getWeatherConfig().subscribe(json => {
      this.parseWeatherConfig(json);
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

  parseWeatherConfig(json): void {
    this.geocodeAPI = json.geocodeApi;
    this.configGeocodeAPI = this.geocodeAPI;
    this.geocode.setApi(this.geocodeAPI);
    this.cityName = json.location;
    this.configCityName = this.cityName;
    this.searchCity();
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

  saveLocation(): void {
    /*this.backend.setWeatherParameter('location', this.location.properties.name).subscribe(json =>
    {
      this.parseWeatherConfig(json);
    });
    this.backend.setWeatherParameter('coordinates', this.location.geometry.coordinates).subscribe(json =>
    {
      this.parseWeatherConfig(json);
    });*/
    this.backend.setWeatherParameters(
      [
        {parameter: 'location', value: this.location.properties.name},
        {parameter: 'longitude', value: this.location.geometry.coordinates[0]},
        {parameter: 'latitude', value: this.location.geometry.coordinates[1]}
      ]).subscribe(json =>
    {
      this.parseWeatherConfig(json);
    });

  }

  saveGeocodeApi(): void {
    this.backend.setWeatherParameter('geocodeApi', this.geocodeAPI).subscribe(json =>
    {
      this.parseWeatherConfig(json);
    });
  }
}
