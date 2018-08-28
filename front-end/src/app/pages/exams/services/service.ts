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

  export interface Admno {
    title: string;
    editable: boolean;
    type: string;
  }
  
  export interface Name {
    title: string;
    editable: boolean;
    type: string;
  }
  
  export interface Score {
    title: string;
    editable: boolean;
    type: string;
  }
  
  export interface Columns {
    admno: Admno;
    name: Name;
    score: Score;
  }
  
  export interface Rows {
    admno: string;
    name: string;
    score?: number;
  }
  
  export interface SmartTable {
    columns: Columns;
    rows: Rows[];
  }
  export interface ExamRecordResponse{
    role?:Role;
    exam?:Exam;
    student?:Rows
  }