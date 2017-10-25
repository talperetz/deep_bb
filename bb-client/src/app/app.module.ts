import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import {NgbModule} from "@ng-bootstrap/ng-bootstrap";
import {TwitterComponent} from "./twitter/twitter.component";
import { RouterModule, Routes } from '@angular/router';
import { BbMainComponent } from './bb-main/bb-main.component';

const appRoutes: Routes = [
  { path: 'tweet', component: TwitterComponent},
  { path: 'main', component: BbMainComponent},
  { path: '',
    redirectTo: '/main',
    pathMatch: 'full'
  },
  { path: '**', component: BbMainComponent}
];

@NgModule({
  declarations: [
    AppComponent,
    TwitterComponent,
    BbMainComponent
  ],
  imports: [
    BrowserModule,
    NgbModule.forRoot(),
    RouterModule.forRoot(appRoutes)
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
