import {Component, OnInit, ViewChild} from '@angular/core';

@Component({
  selector: 'app-about',
  templateUrl: './about.component.html',
  styleUrls: ['./about.component.css']
})
export class AboutComponent implements OnInit {

  @ViewChild('qwe') asd;
  private createScript() {
    var script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = "//platform.linkedin.com/in.js";
    var head = document.getElementsByTagName("head")[0];
    head.appendChild(script);

    let x = ['https://www.linkedin.com/in/david-limkys-9907ba8b', 'https://www.linkedin.com/in/demibenari', 'https://www.linkedin.com/in/dor-peretz-166464141', 'https://www.linkedin.com/in/ran-shamay',  'https://www.linkedin.com/in/tal-per'];

    x.forEach(z => {
      let script = document.createElement('script');
      script.type = 'IN/MemberProfile';
      script.setAttribute('data-id', z);
      script.setAttribute('data-format', 'inline');
      script.setAttribute('data-related', 'false');
      this.asd.nativeElement.appendChild(script);
    })
  }

  ngOnInit() {
    this.createScript();
  }

}
