import {Component, OnInit} from '@angular/core';
import {Http, Response} from "@angular/http";

@Component({
  selector: 'app-speech',
  templateUrl: './speech.component.html',
  styleUrls: ['./speech.component.css']
})
export class SpeechComponent implements OnInit {

  public _speech: string;

  constructor(private _http: Http) {
  }

  ngOnInit() {
  }

  generateSpeech() {
    this._http.get("http://35.189.250.254:3000/speech").subscribe((res: any) => {
      if (res.ok) {
        this._speech = JSON.parse(res._body).speech;
      }
    });
  }

}
