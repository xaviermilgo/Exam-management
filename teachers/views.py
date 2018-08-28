from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
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
        data["form_exams"].append({"form":f.name,"exams":list({"id":e.id,"exam_name":e.__str__()} for e in f.exams.all())})
    return Response(data)

@api_view(['POST'])
def get_selected_records(request):
    print(request.data)
    return Response({"good","good"})