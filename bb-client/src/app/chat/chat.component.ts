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
//
  }

  ngOnInit() {
  }

  public post(event) {
    let text;
    if (event.target)
      text = event.target.value;
    else
      text = event;

    if (!text || text.trim().length === 0) {
      return;
    }

    this.messages.push({text: text, color: '#000'});

    this.chatService.getAnswer(text).subscribe((answer: any) => {
      let response = JSON.parse(answer._body).response;
      this.messages.push({text: response, color: '#0863bb'});

      //   responsiveVoice.speak(response, "UK English Male", {pitch: .7, range: 1});

      event.target.value = '';
      event.target.disabled = '';
    });

    event.target.disabled = 'disabled';
    event.target.value = 'Typing...';
  }

  public getMessages() {
    return this.messages.slice(Math.max(this.messages.length - 10, 0))
  }

  public ngAfterViewChecked() {
  }
}
