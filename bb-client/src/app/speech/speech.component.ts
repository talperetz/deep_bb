import {Component, OnInit} from '@angular/core';
import {Http, Response} from "@angular/http";

@Component({
  selector: 'app-speech',
  templateUrl: './speech.component.html',
  styleUrls: ['./speech.component.css']
})
export class SpeechComponent implements OnInit {

  public _speech: string = "asdASDas" +
    "dascsad" +
    "asd" +
    "asd" +
    "asdasdasd asd asd asfd asf sda g earg erh  fh hs " +
    "h" +
    "f h sdfh fdsh fd g fg erh rt hrg ng fn b fd hfd hs dfg dfg ads" +
    "gd g dag adg fdg fdsgfdskglndflskg f dgf dgnk fdlgj fdgj dfg lsdfg dsfjlg a'gd'sagda gdg" +
    "gdGJD GKJA,DSFBASLKJBw;fbgEOFBN;klfbjklsdblkjsbvkzcx.jvbnds sdf " +
    "dsf ajn";

  constructor(private _http: Http) {
  }

  ngOnInit() {
  }

  generateSpeech() {
    this._http.get("hostname/speech").subscribe((res: Response) => {
      if (res.ok) {
        this._speech = res.toString();
      }
    });
  }

}
