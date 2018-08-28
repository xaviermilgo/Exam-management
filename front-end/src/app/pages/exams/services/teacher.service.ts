import { Injectable } from '@angular/core';
import {HttpClient,HttpHeaders, HttpErrorResponse} from '@angular/common/http'
import { NbAuthService } from '@nebular/auth';
import {environment} from "../../../../environments/environment";


export interface Role {
  id: number;
  subject: string;
  form: string;
  class: string;
  role:string;
}

export interface Exam {
  id: number;
  exam_name: string;
}

export interface FormExam {
  form: string;
  exams: Exam[];
}

export interface Teacher {
  name: string;
  phone_number: string;
  roles: Role[];
  form_exams: FormExam[];
}
export interface ExamFormResponse{
  role?:Role;
  exam?:Exam;
}

@Injectable({
  providedIn: 'root'
})
export class TeacherService {

  errorNotification:string
  errorBool:boolean=false

  teacherData:Teacher;

  private _headers = new HttpHeaders();
  private authToken:string;

  teacherUrl:string =environment.apiEndPoint +"api-get-teacher"
  examPostUrl:string = environment.apiEndPoint + "api-post-selected-exam"

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
      this.handleError(error)
      reject()
    })
    })
    return promise   
  }
  postExamForm(examFormData:ExamFormResponse){
    const headers = this._headers.append('Authorization','JWT '+this.authToken);
    let promise=new Promise((resolve,reject)=>{
      this.http.post(this.examPostUrl,examFormData,{headers:headers}).toPromise().then(myResponse=>{
        console.log(myResponse)
        resolve()
      },
    error=>{
      console.log(error)
      this.handleError(error)
      reject()
    })
    })
    return promise   
  }

  private handleError(error: HttpErrorResponse) {
    if (error.error instanceof ErrorEvent) {
      this.errorBool=true
      this.errorNotification="Error occured, try again"
      console.error('An error occurred:', error.error.message);
    } else if(error.status == 404) {
      this.errorBool=true
      this.errorNotification="Error 404"
    } else if(error.status == 403) {
      this.errorBool=true
      this.errorNotification="Access denied, try logging in again"
    }
}
}