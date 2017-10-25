import {Component, OnInit} from '@angular/core';
import {ChatService} from "./chat.service";

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})
export class ChatComponent implements OnInit {

  public messages: any[] = [];

  constructor(private chatService: ChatService) {
  }

  ngOnInit() {
  }

  public post(event) {
    const text = event.target.value;

    if (!text || text.trim().length === 0){
      return;
    }

    this.messages.push({text: text, color: '#000'});

    this.chatService.getAnswer(text).then(answer => this.messages.push({text: answer, color: '#000'}));

    event.target.value = '';
  }

  public getMessages() {
    return this.messages.slice(Math.max(this.messages.length - 5, 0))
  }

  private getColor() {
  }

}
