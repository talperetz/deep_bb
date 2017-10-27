import {Component, OnInit} from '@angular/core';
import {Http, Response} from "@angular/http";
import Chart from 'chart.js';

@Component({
  selector: 'app-speech',
  templateUrl: './speech.component.html',
  styleUrls: ['./speech.component.css']
})
export class SpeechComponent implements OnInit {

  public _speech: string;
  public isPlaying = true;


  barChartLabels = [];
  barChartData = [{data:[]}];
  colors = [{
    backgroundColor:'rgba(77, 182, 172, .7)'
  }];

  constructor(private _http: Http) {
  }

  ngOnInit() {
  }

  generateSpeech() {
    this._http.get("http://35.189.250.254:3000/speech").subscribe((res: any) => {
      if (res.ok) {
        this._speech = JSON.parse(res._body).speech;
        let statisctics = JSON.parse(res._body).statistics;
        let sbvc = JSON.parse(res._body).sort_by_values_counts;
        let statistics_words = JSON.parse(res._body).statistics_words;

        this.barChartLabels = statistics_words;
        this.barChartData[0].data = sbvc;
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
