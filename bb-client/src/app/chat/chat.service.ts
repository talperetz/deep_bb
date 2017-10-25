import { Injectable } from '@angular/core';

@Injectable()
export class ChatService {

  constructor() { }

  public getAnswer(question:string){
    return new Promise(resolve => {
      resolve('fuck off');
    })
  }
}
