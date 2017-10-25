import { Component, OnInit } from '@angular/core';
import {Http} from "@angular/http";

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

  // TODO : change hostname
  generateTweet() {
    this._http.post("hostname/tweet", {});
  }
  ngOnInit() {

  }

}
