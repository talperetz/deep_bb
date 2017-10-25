import {Component, OnInit, HostListener} from '@angular/core';

@Component({
  selector: 'app-bb-main',
  templateUrl: './bb-main.component.html',
  styleUrls: ['./bb-main.component.css']
})
export class BbMainComponent implements OnInit {

  public isHover = false;
  constructor() { }

  ngOnInit() {
  }


  @HostListener('mouseover')
  onMouseOver() {
    this.isHover = true;
  }

  @HostListener('mouseout')
  onMouseOut() {
    this.isHover = false;
  }

}
