import { Component, OnInit } from '@angular/core';
import {Http, Response} from "@angular/http";

@Component({
  selector: 'app-twitter',
  templateUrl: './twitter.component.html',
  styleUrls: ['./twitter.component.css']
})
export class TwitterComponent implements OnInit {

  constructor(private _http : Http) {
    var script = document.createElement('script');
    script.src = '/assets/widgets.js';
    script.type = 'text/javascript';
    var head = document.getElementsByTagName("head")[0];
    head.appendChild(script);
  }

  generateTweet() {
    this._http.post("http://35.189.250.254:3000/tweet", {}).subscribe((res : Response) => {
      console.log(res.toString());
    });
  }
  ngOnInit() {

  }

}
