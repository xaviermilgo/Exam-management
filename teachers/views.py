from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views import View
from django.conf import settings
from django.http import HttpResponse,JsonResponse,HttpResponseBadRequest
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Class,Form,Subjects,TeacherRoles,Student,Exam,Streams,Records,Teacher, OverallGrade,Results
import time,json
from operator import itemgetter
import os


@login_required(login_url='/admin')
def results_list(request):
    try:
        type_=request.GET.get("type")
        exam_id=int(request.GET.get("exam_id"))
        type_id=int(request.GET.get("type_id"))
        exam=get_object_or_404(Exam,pk=exam_id)
        if not type_ in ["class","form"]:
            return HttpResponseBadRequest("Bad request")
        elif type_ == "class":
            obj=get_object_or_404(Class,pk=type_id)
        elif type_ == "form":
            obj=get_object_or_404(Form,pk=type_id)
        context={"type":type_,"exam":exam,"dataObj":obj}
        return render(request,"admin/view_results_lists.html",context)
    except Exception as err:
        print(err)
        return HttpResponseBadRequest("Bad request")

@login_required(login_url='/admin')
def select_exam(request):
    exams=Exam.objects.all().order_by("-created_at")
    return render(request,"admin/select_exam_view.html",{"exams":exams})
    
@login_required(login_url='/admin')
def select_class_form(request):
    try:
        exam_id=int(request.GET.get('exam_id'))
        exam=Exam.objects.get(pk=exam_id)
    except Exception as err:
        return HttpResponseBadRequest("Bad request")
    forms= exam.form.all()
    c={i:[j for j in i.classes.all()] for i in forms}
    return render(request,"admin/select_class_form.html",{"class_forms":c,"exam":exam})


class ResultsView(LoginRequiredMixin,View):
    login_url="/admin"
    def get(self, request, *args, **kwargs):
        # self.request.GET.get('order_by')
        # self.teacher = Teacher.objects.get(user=request.user)
        self.post_data=request.GET
        if self.validate_request():
            if self.get_records_postgres(): #self.get_records_json() if not using postgres
                return JsonResponse(self.sorted_results)
            return JsonResponse({'error': 'Server error'}, status=500)
        return JsonResponse({'error': 'Bad request'}, status=400)  

    def validate_request(self):
        try:
            # types can only be form or class
            # {"type":"class/form","type_id":"id","exam_id":"id"}
            self.type_=self.post_data.get("type")
            self.exam_id=int(self.post_data.get("exam_id"))
            self.type_id=int(self.post_data.get("type_id"))
            self.regrade=self.post_data.get("regrade")
            self.exam=Exam.objects.get(id=self.exam_id)
            if self.regrade not in ["false","true"]:
                return False
            if self.type_ not in ["class","form"]:
                return False
            elif self.type_ == "class":
                self.students_class=Class.objects.get(id=self.type_id)
                self.students_form=self.students_class.form
                self.students_list= Student.objects.filter(class_name=self.students_class)
                self.records= Records.objects.filter(exam=self.exam,student__class_name=self.students_class)
            elif self.type_ == "form":
                self.students_form = Form.objects.get(id=self.type_id)
                self.students_list= Student.objects.filter(class_name__form=self.students_form)
                self.records= Records.objects.filter(exam=self.exam,student__class_name__form=self.students_form)
            return True
        except Exception as err:
            print(err)
            return False

    def get_records_json(self):
        start=time.time()
        j_path=os.path.join(settings.BASE_DIR, 'results')
        if self.regrade=="false":
            if not os.path.exists(j_path):
                os.mkdir(j_path)
            if os.path.exists("{}/{}_{}_{}.json".format(j_path,self.type_,self.type_id,self.exam_id)):
                with open("{}/{}_{}_{}.json".format(j_path,self.type_,self.type_id,self.exam_id),"r") as jfile:
                    self.sorted_results=json.load(jfile)
                print("Reading from json, time taken:{}".format(time.time()-start))
                return True
    
        if not self.exam.editable: return False
        if self.get_records_from_db():
            self.add_student_positions()
            with open("{}/{}_{}_{}.json".format(j_path,self.type_,self.type_id,self.exam_id),"w") as jfile:
                json.dump(self.sorted_results,jfile)
            print("Reading from database, time taken:{}".format(time.time()-start))
            return True
        return False        

    def get_records_postgres(self):
        start=time.time()
        if self.regrade=="false":
            r=Results.objects.filter(type_name=self.type_,type_id=self.type_id,exam=self.exam)
            if r.exists():
                self.sorted_results=json.loads(r[0].results)
                print("JsonField, time taken:{}".format(time.time()-start))
                return True
        if not self.exam.editable: return False
        if self.get_records_from_db():
            self.add_student_positions()
            Results.objects.update_or_create(type_name=self.type_,type_id=self.type_id,exam=self.exam,results=json.dumps(self.sorted_results))
            print("Reading from database, time taken:{}".format(time.time()-start))
            return True
        return False

    def get_records_from_db(self):
        self.unsorted_results=[]
        subjects= list(Subjects.objects.all())
        sub_abbr=list(j.abbreviation for j in subjects)
        overall_grades= OverallGrade.objects.all()
        minimum_subjects= self.students_form.minimum_subjects
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
                    std[sub]=""
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
        self.sorted_results={"data":sorted(self.unsorted_results,key=itemgetter("avg"),reverse=True)}
        return True

    def add_student_positions(self):
        initPoints=0
        stdCount=0
        pos=1
        for i in self.sorted_results["data"]:
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