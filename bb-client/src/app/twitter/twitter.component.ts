import {Component, OnInit} from '@angular/core';
import {Http, Response} from "@angular/http";
import {Router} from "@angular/router";

@Component({
    selector: 'app-twitter',
    templateUrl: './twitter.component.html',
    styleUrls: ['./twitter.component.css']
})
export class TwitterComponent implements OnInit {

    public isUpdate = true;

    constructor(private _http: Http, private router: Router) {
        this.createScript();
    }

    private createScript() {
        var script = document.createElement('script');
        script.type = 'text/javascript';
        script.src = "/assets/widgets.js"
        script.id = "1";
        var head = document.getElementsByTagName("head")[0];
        head.appendChild(script);
    }

    generateTweet() {
        this._http.post("http://35.189.250.254:3000/tweet", {}).subscribe((res: Response) => {
            console.log(res.toString());
        });

        let script = document.getElementById("1");
        script.parentNode.removeChild(script);
        this.isUpdate = false;
        setTimeout(() => {
            this.createScript();
           this.isUpdate = true;
        }, 2000);
    }

    ngOnInit() {

    }

}
