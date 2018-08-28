import { Component, OnDestroy,OnInit } from '@angular/core';
import { NbThemeService } from '@nebular/theme';
import { ToasterService, ToasterConfig, Toast, BodyOutputType } from 'angular2-toaster';
import {TeacherService,Teacher,Role,Exam,ExamFormResponse} from './services/teacher.service';

export interface Notification {
  type:string;
  title: string;
  message:string;
}

@Component({
  selector: 'ngx-exams',
  templateUrl: './exams.component.html',
  styleUrls: ['./exams.component.scss']
})
export class ExamsComponent implements OnDestroy,OnInit {
  notification:Notification
  currentTheme: string;
  themeSubscription: any;
  showExamForm1:boolean=true
  showExamForm2:boolean=false;
  examYear:string;
  examName:string;
  teacherRole:Role;
  teacher:Teacher;
  formExams: Exam[];
  selectedFormExam:Exam;
  examResponseForm:ExamFormResponse;
   
  constructor(private themeService: NbThemeService,
              private teacherService:TeacherService){
    this.themeSubscription = this.themeService.getJsTheme().subscribe(theme => {
      this.currentTheme = theme.name;
    });
    this.examResponseForm={}
  }

  loadTeacher(){
    this.teacherService.getTeacher().then(()=>{
      if(this.teacherService.errorBool){
        this.notification = {type:"error",title:"error",message:this.teacherService.errorNotification}
        this.teacherService.errorBool=false
        this.teacherService.errorNotification=''
      }
      else{
        this.teacher=this.teacherService.teacherData
      }
    })
  }
  submitExamResponse(){
    this.teacherService.postExamForm(this.examResponseForm).then(()=>{

    })
  }
  getForm1(){
    console.log(this.teacherRole)
    this.examResponseForm.role=this.teacherRole
    for(var i=0; i < this.teacher.form_exams.length; i++){
      if(this.teacherRole.form == this.teacher.form_exams[i].form){
        this.formExams=this.teacher.form_exams[i].exams
      }
    }
    this.showExamForm1=false
    this.showExamForm2=true
  }

  getForm2(){
    console.log(this.selectedFormExam)
    this.examResponseForm.exam=this.selectedFormExam
    this.submitExamResponse()
  }

  ngOnDestroy(){
    this.themeSubscription.unsubscribe();
  }

  ngOnInit(){
    this.loadTeacher()
  }

}

