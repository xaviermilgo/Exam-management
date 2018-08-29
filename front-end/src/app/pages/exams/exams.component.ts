import { Component, OnDestroy,OnInit } from '@angular/core';
import { NbThemeService } from '@nebular/theme';
import { ToasterService, ToasterConfig, Toast, BodyOutputType } from 'angular2-toaster';
import { SmartTableService } from '../../@core/data/smart-table.service';
import { LocalDataSource } from 'ng2-smart-table';
import {Router} from '@angular/router'
import {TeacherService} from './services/teacher.service';
import {Teacher,Role,Exam,ExamFormResponse,Columns,Rows,ExamRecordResponse} from './services/service'


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
  showSmartTable:boolean=false;
  examYear:string;
  examName:string;
  teacherRole:Role;
  teacher:Teacher;
  formExams: Exam[];
  selectedFormExam:Exam;
  examResponseForm:ExamFormResponse;
  tableData: Rows[];
  tableColumns:Columns;
  tableSettings:any;
  examRecord:ExamRecordResponse;


  constructor(private themeService: NbThemeService,
              private teacherService:TeacherService,
              private router:Router,
              ){
    this.themeSubscription = this.themeService.getJsTheme().subscribe(theme => {
      this.currentTheme = theme.name;
    });
    this.examResponseForm={}
    this.examRecord={}
    this.teacher={}
  }

  loadTeacher(){
    this.teacherService.getTeacher().then(()=>{
      this.teacher=this.teacherService.teacherData
    }).catch(error =>{
      this.notification = {type:"error",title:"Error",message:"Try again or check internet connection"}
    })
  }

  submitExamResponse(){
    this.teacherService.postExamForm(this.examResponseForm).then(()=>{
        this.tableColumns=this.teacherService.smartTableData.columns
        this.tableData=this.teacherService.smartTableData.rows
        this.showExamForm2=false
        this.tableSettings = {
          hideSubHeader:false,
          actions:{
            add: false,
            delete:false,
          },
          edit: {
            editButtonContent: '<i class="nb-edit"></i>',
            saveButtonContent: '<i class="nb-checkmark"></i>',
            cancelButtonContent: '<i class="nb-close"></i>',
            confirmSave: true, 
          },
          columns: this.tableColumns,
        };
        this.showSmartTable= true
    }).catch(error =>{
      this.notification = {type:"error",title:"Error",message:"unable to retrieve table, try again or check internet connection"}
    })
  }

  submitRecord(record:ExamRecordResponse){
    this.teacherService.postExamRecord(record).then(()=>{
      this.notification = {type:"success",title:"success",message:"Record saved"}
    }).catch(error =>{
      this.notification = {type:"error",title:"Server error",message:"record not saved,try again or check internet connection"}
    })
  }

  submitForm1(){
    if(this.teacherRole){
      this.examResponseForm.role=this.teacherRole
      for(var i=0; i < this.teacher.form_exams.length; i++){
        if(this.teacherRole.form == this.teacher.form_exams[i].form){
          this.formExams=this.teacher.form_exams[i].exams
        }
      }
      this.showExamForm1=false
      this.showExamForm2=true
    }
  }

  submitForm2(){
    if(this.selectedFormExam){
      this.examResponseForm.exam=this.selectedFormExam
      this.submitExamResponse()
    }
  }
 
  validateScore(newData,prevData){
    if(newData["score"]==prevData["score"]){
      this.notification = {type:"error",title:"error",message:"No change detected"}
      return false
    }
    var reg = new RegExp(/^\d*$/)
    if(reg.test(newData["score"]) != true){
      this.notification = {type:"error",title:"error",message:"Input must be a number"}
      return false
    }
    var score = parseInt(newData["score"])
    if(score>100 || score<0){
      this.notification = {type:"error",title:"error",message:"Input must between range 0-100"}
      return false
    }
    return true
  }

  saveNewScore(event){
    console.log(event["newData"])
    var state=this.validateScore(event["newData"],event["data"])
    if(state===true){
      this.examRecord.exam=this.selectedFormExam
      this.examRecord.role=this.teacherRole
      this.examRecord.student=event["newData"]
      this.submitRecord(this.examRecord)
      event.confirm.resolve();
    }    
  }
  goHome(){
    // reset
    this.teacher={}
    this.formExams=[]
    this.loadTeacher()
    this.examResponseForm={}
    this.examRecord={}
    this.showSmartTable=false
    this.showExamForm1=true
    this.showExamForm2=false
  }

  ngOnDestroy(){
    this.themeSubscription.unsubscribe();
  }

  ngOnInit(){
    this.loadTeacher()
  }

}

