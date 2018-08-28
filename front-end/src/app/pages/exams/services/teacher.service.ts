import { Injectable } from '@angular/core';
import {HttpClient,HttpHeaders, HttpErrorResponse} from '@angular/common/http'
import { NbAuthService } from '@nebular/auth';
import {environment} from "../../../../environments/environment";
import {Teacher,ExamFormResponse,SmartTable,ExamRecordResponse} from "./service"

@Injectable({
  providedIn: 'root'
})
export class TeacherService {

  teacherData:Teacher;
  smartTableData:SmartTable;

  private _headers = new HttpHeaders();
  private authToken:string;

  teacherUrl:string =environment.apiEndPoint +"api-get-teacher"
  examPostUrl:string = environment.apiEndPoint + "api-post-selected-exam"
  recordPostUrl:string = environment.apiEndPoint + "api-post-new-record"

  constructor(private http:HttpClient,private authService:NbAuthService) { 
    this.authToken=this.authService.getToken()["value"]["token"]
  }

  getTeacher(){
    const headers = this._headers.append('Authorization','JWT '+this.authToken);
    let promise=new Promise((resolve,reject)=>{
      this.http.get<Teacher>(this.teacherUrl,{headers:headers}).toPromise().then(myResponse=>{
        this.teacherData=myResponse
        console.log(this.teacherData)
        resolve()
      },
    error=>{
      console.log(error)
      reject()
    })
    })
    return promise   
  }

  postExamRecord(record:ExamRecordResponse){
    const headers = this._headers.append('Authorization','JWT '+this.authToken);
    let promise=new Promise((resolve,reject)=>{
      this.http.post(this.recordPostUrl,record,{headers:headers}).toPromise().then(myResponse=>{
        resolve()
      },
    error=>{
      console.log(error)
      reject()
    })
    })
    return promise  
  }

  postExamForm(examFormData:ExamFormResponse){
    const headers = this._headers.append('Authorization','JWT '+this.authToken);
    let promise=new Promise((resolve,reject)=>{
      this.http.post<SmartTable>(this.examPostUrl,examFormData,{headers:headers}).toPromise().then(myResponse=>{
        this.smartTableData=myResponse
        console.log(this.smartTableData)
        resolve()
      },
    error=>{
      console.log(error)
      reject()
    })
    })
    return promise   
  }
}