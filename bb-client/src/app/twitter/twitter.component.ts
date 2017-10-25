import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-twitter',
  templateUrl: './twitter.component.html',
  styleUrls: ['./twitter.component.css']
})
export class TwitterComponent implements OnInit {

  constructor() {
  }

  ngOnInit() {
    var script = document.createElement('script');
    script.src = '/assets/widgets.js';
    script.type = 'text/javascript';
    var head = document.getElementsByTagName("head")[0];
    head.appendChild(script);
  }

}
