import re
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Class,Form,Subjects,TeacherRoles,Student,Exam,Streams,Records,Teacher, OverallGrade
import time
from operator import itemgetter

def print_headers(request):
    regex = re.compile('^HTTP_')
    x=dict((regex.sub('', header), value) for (header, value) 
        in request.META.items() if header.startswith('HTTP_'))
    print(x)

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_teacher(request):
    teacher = Teacher.objects.get(user=request.user)
    data={"name":request.user.username,"phone_number":teacher.phone_number,"roles":[],"form_exams":[]}
    forms =list(set([i for i in Form.objects.all()]))
    for f in forms:
        data["form_exams"].append({"form":f.name,"exams":list({"id":e.id,
            "exam_name":e.__str__()} for e in f.exams.filter(editable=True))})
    if request.user.is_superuser:
        for i in TeacherRoles.objects.all():
            data["roles"].append({"id":i.id,"subject":i.subject.__str__(),
                    "form":i.class_name.form.name,"class":i.class_name.__str__(),"role":i.__str__()})
    else:  
        for i in teacher.roles.all():
            data["roles"].append({"id":i.id,"subject":i.subject.__str__(),"form":i.class_name.form.name,
                "class":i.class_name.__str__(),"role":i.__str__()})
    return Response(data)

class GetRecordsView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        self.teacher = Teacher.objects.get(user=request.user)
        self.post_data=request.data
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
                if r_.exists():
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
            r=Records.objects.filter(student=self.student,student__class_name=self.role.class_name,
                exam=self.exam,subject=self.role.subject)
            if not r.exists():
                r=Records(student=self.student,exam=self.exam,
                subject=self.role.subject,score=self.student_score)
                r.set_grade()
            else:
                r=r[0]
                r.score=self.student_score
                r.set_grade()
            r.save()

            return True
        except Exception as err:
            print(err)
            return False
 
class GetResultsView(APIView):
    # permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        # self.teacher = Teacher.objects.get(user=request.user)
        self.post_data=request.data
        if self.validate_request():
            if self.get_records_from_db():
                self.add_student_positions()
                return Response(self.sorted_results)
            return Response({'error': 'Server error'}, status=500)
        return Response({'error': 'Bad request'}, status=400)  


    def validate_request(self):
        try:
            # types can only be form or class
            # {"type":"class/form","type_id":"id","exam_id":"id"}
            self.type=self.post_data.get("type")
            self.exam_id=int(self.post_data.get("exam_id"))
            self.type_id=int(self.post_data.get("type_id"))
            self.exam=Exam.objects.get(id=self.exam_id)
            if self.type not in ["class","form"]:
                return False
            elif self.type == "class":
                self.students_class=Class.objects.get(id=self.type_id)
                self.students_form=self.students_class.form
                self.students_list= Student.objects.filter(class_name=self.students_class)
                self.records= Records.objects.filter(exam=self.exam,student__class_name=self.students_class)
            elif self.type == "form":
                self.students_form = Form.objects.get(id=self.type_id)
                self.students_list= Student.objects.filter(class_name__form=self.students_form)
                self.records= Records.objects.filter(exam=self.exam,student__class_name__form=self.students_form)
            return True
        except Exception as err:
            print(err)
            return False

    def get_records_from_db(self):
        subjects= list(Subjects.objects.all())
        sub_abbr=list(j.abbreviation for j in subjects)
        overall_grades= OverallGrade.objects.all()
        minimum_subjects= self.students_form.minimum_subjects
        self.unsorted_results=[]
        start = time.time()
        # for the meantime till i get a better solution
        for s in list(self.students_list):
            std={"admno":s.admno,"name":s.name}
            totalP=0
            records_count=0
            # and here is our algorithm killer :(
            for sub in  sub_abbr:
                # we are hitting the db O(n^2), we need help
                r=self.records.filter(student=s,subject__abbreviation =sub)
                if r.exists():
                    records_count +=1
                    totalP +=r[0].grade.points
                    std[sub]=r[0].score
                    # std["subjects"][k]["grade"]=r[0].grade.name
                else:
                    std[sub]=None
            std["points"]=totalP
            if records_count<minimum_subjects:
                std["avg"]=0
                std["grade"]="X"
            else:            
                avgPoints=totalP/minimum_subjects
                std["avg"]=float("{0:.2f}".format(avgPoints))
                grade=overall_grades.get(high_points__gte= avgPoints,low_points__lte= avgPoints)
                std["grade"]=grade.name
            self.unsorted_results.append(std)
        self.sorted_results=sorted(self.unsorted_results,key=itemgetter("avg"),reverse=True)
        print("Time taken: {}".format(time.time()-start))
        return True

    def add_student_positions(self):
        initPoints=0
        stdCount=0
        pos=1
        for i in self.sorted_results:
            stdCount +=1
            # for pos 1
            if i["avg"]>initPoints:
                i["pos"]=stdCount
            elif i["avg"]==initPoints:
                i["pos"]=pos
            elif i["avg"]<initPoints:
                pos =stdCount
                i["pos"]=pos
            initPoints=i["avg"]



    




{"type":"form","type_id":"1","exam_id":"1"}