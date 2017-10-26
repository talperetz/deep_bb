import {Component, OnInit} from '@angular/core';
import {Http, Response} from "@angular/http";

@Component({
  selector: 'app-speech',
  templateUrl: './speech.component.html',
  styleUrls: ['./speech.component.css']
})
export class SpeechComponent implements OnInit {

  public _speech: string;
  public isPlaying = true;
  constructor(private _http: Http) {
  }

  ngOnInit() {
  }

  generateSpeech() {
    this._http.get("http://35.189.250.254:3000/speech").subscribe((res: any) => {
      if (res.ok) {
        this._speech = JSON.parse(res._body).speech;
        responsiveVoice.speak(this._speech, "UK English Male", {pitch: .7, range: 1});
      }

    });
  }

  togglePlaying(){
    if(this.isPlaying) {
      responsiveVoice.pause();
    }else{
      responsiveVoice.resume();
    }

    this.isPlaying = !this.isPlaying;
  }
}
