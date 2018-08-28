from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import Class,Form,Subjects,TeacherRoles,Student,Exam,Streams,Records,Teacher


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_teacher(request):
    teacher = Teacher.objects.get(user=request.user)
    forms =list(set([i.class_name.form for i in teacher.roles.all()]))
    data={"name":request.user.username,"phone_number":teacher.phone_number,"roles":[],"form_exams":[]}
    for i in teacher.roles.all():
        data["roles"].append({"id":i.id,"subject":i.subject.__str__(),"form":i.class_name.form.name,"class":i.class_name.__str__(),"role":i.__str__()})
    
    for f in forms:
        data["form_exams"].append({"form":f.name,"exams":list({"id":e.id,"exam_name":e.__str__()} for e in f.exams.filter(editable=True))})
    return Response(data)

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def get_selected_records(request):
    print(request.data)
    return Response({"good","good"})


class GetRecordsView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        self.teacher = Teacher.objects.get(user=request.user)
        self.post_data=request.data
        print(self.post_data)
        if self.validate_data():
            if self.table_data():
                return Response(self.smart_table)
            return Response({'error': 'Server error'}, status=500)
        return Response({'error': 'Bad request'}, status=400)        

    def validate_data(self):
        try:
            role_id=self.post_data.get("role")["id"]
            self.role=TeacherRoles.objects.get(id=role_id)
            exam_id = self.post_data.get("exam")["id"]
            self.exam= Exam.objects.get(id=exam_id)
            return True
        except Exception as err:
            print(err)
            return False

    def table_data(self):
        try:
            self.students=Student.objects.filter(class_name=self.role.class_name)
            self.smart_table={"columns":{
                "admno":{"title":"Adm No","editable":False,"type":"number"},
                "name":{"title":"Name","editable":False,"type":"string"},
                "score":{"title":self.role.subject.name,"editable":True,"type":"number"}
                    },
                "rows":[]
                }
            self.records= Records.objects.filter(student__class_name=self.role.class_name,exam=self.exam,subject=self.role.subject)
            for student in self.students:
                s={"admno":student.admno,"name":student.name}
                r_=self.records.filter(student__admno=student.admno)
                if r_:
                    s["score"]=r_[0].score
                else:
                    s["score"]=None
                self.smart_table["rows"].append(s)
            return True
        except Exception as err:
            print(err)
            return False

class saveNewRecord(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        self.teacher = Teacher.objects.get(user=request.user)
        self.post_data=request.data
        print(self.post_data)
        if self.validate_data():
            if self.update_score():
                return Response({"success":"record updated"})
            return Response({'error': 'Server error'}, status=500)
        return Response({'error': 'Bad request'}, status=400)  

    def validate_data(self):
        try:
            role_id=self.post_data.get("role")["id"]
            self.role=TeacherRoles.objects.get(id=role_id)
            exam_id = self.post_data.get("exam")["id"]
            self.exam= Exam.objects.get(id=exam_id)
            student_adm=self.post_data.get("student")["admno"]
            self.student=Student.objects.get(admno=student_adm)
            self.student_score=int(self.post_data.get("student")["score"])
            if self.student_score<0 or self.student_score > 100:
                return False
            return True
        except Exception as err:
            print(err)
            return False
    def update_score(self):
        try:
            s=Records.objects.filter(student=self.student,student__class_name=self.role.class_name,
                exam=self.exam,subject=self.role.subject).update(score=self.student_score)
            if not s:
                Records.objects.create(student=self.student,exam=self.exam,
                subject=self.role.subject,score=self.student_score)
            return True
        except Exception as err:
            print(err)
            return False



