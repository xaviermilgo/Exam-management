from .models import *
import forgery_py
import random
def fake_students_per_class(n,admLow,admHigh):
    classes=Class.objects.all()
    for class_ in classes:
        count=0
        while count<n:
            admno=random.randrange(admLow,admHigh)
            if not Student.objects.filter(admno=admno):
                Student.objects.create(admno=admno,class_name=class_,name=forgery_py.name.full_name())
                count +=1



def fake_subject_scores(form_id,exam_id):
    subjects=Subjects.objects.all()
    form_=Form.objects.get(pk=form_id)
    exam=Exam.objects.get(pk=exam_id)
    students=Student.objects.filter(class_name__form=form_)
    for s in students:
        sbj_count=0
        # fuck you i know its O(n^2) its not like am doing this for fun
        while sbj_count<form_.minimum_subjects:
            try:
                r=Records(subject=subjects[sbj_count],student=s,score=random.randrange(1,100),exam=exam)
                r.set_grade()
                r.save()
            except:
                pass
            sbj_count +=1



