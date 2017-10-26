import { Injectable } from '@angular/core';
import {Http, Response} from "@angular/http";

@Injectable()
export class ChatService {

  constructor(private http: Http) { }

  public getAnswer(question:string){
    return this.http.post("http://35.189.250.254:3000/chat", {msg:question});
  }
}
