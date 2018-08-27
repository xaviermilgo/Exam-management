import { Component, OnDestroy,OnInit } from '@angular/core';
import { NbThemeService } from '@nebular/theme';

@Component({
  selector: 'ngx-exams',
  templateUrl: './exams.component.html',
  styleUrls: ['./exams.component.scss']
})
export class ExamsComponent implements OnDestroy,OnInit {

  currentTheme: string;
  themeSubscription: any;
  showExamForm1:boolean=true
  showExamForm2:boolean=false
  examYear:string;
  examName:string;
  teacherRole:string;
   
  constructor(private themeService: NbThemeService){
    this.themeSubscription = this.themeService.getJsTheme().subscribe(theme => {
      this.currentTheme = theme.name;
    });
  }

  getForm1(){
    console.log(this.examYear,this.teacherRole)
    this.showExamForm1=false
    this.showExamForm2=true
  }

  getForm2(){
    console.log(this.examName)
  }

  ngOnDestroy(){
    this.themeSubscription.unsubscribe();
  }

  ngOnInit(){
  }

}

