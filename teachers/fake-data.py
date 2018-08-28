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

