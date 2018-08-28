from django.db import models
from django.contrib.auth.models import User
import datetime

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    phone_number=  models.CharField(max_length=10,null=False,unique=True)
    def __str__(self):
        return "{} {}".format(self.user,self.phone_number)


class TeacherRoles(models.Model):
    teacher = models.ForeignKey("Teacher", on_delete=models.CASCADE, null=False,related_name="roles")
    subject = models.ForeignKey("Subjects", on_delete=models.PROTECT,related_name="teacher_roles")
    class_name = models.ForeignKey("Class", on_delete=models.PROTECT,related_name="role")
    
    def __str__(self):
        return "{} {} {}".format(self.teacher.user,self.subject,self.class_name)

    class Meta:
        verbose_name_plural="Teacher Roles"

class Subjects(models.Model):
    name= models.CharField(max_length=255,null=False,unique=True)
    form = models.ManyToManyField("Form",related_name="form_subjects")
    def __str__(self):
        return str(self.name)
    class Meta:
        verbose_name_plural="Subjects"

class Form(models.Model):
    name = models.CharField(max_length=255,null=False,unique=True)

    def __str__(self):
        return "Form {}".format(self.name)

class Streams(models.Model):
    name = models.CharField(max_length=255,null=False,unique=True)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name_plural="Streams"

class Class(models.Model):
    stream = models.ForeignKey("Streams", on_delete=models.PROTECT,related_name="class_name",null=False)
    form=models.ForeignKey("Form", on_delete=models.PROTECT,related_name="classes",null=False)
    def __str__(self):
        return "{} {}".format(self.form, self.stream)

    class Meta:
        verbose_name_plural="Classes"



class Student(models.Model):
    admno = models.CharField(max_length=255,null=False,unique=True)
    name = models.CharField(max_length=255,null=False)
    class_name = models.ForeignKey("Class", on_delete=models.PROTECT,related_name="students",null=False)

    def __str__(self):
        return str(self.admno)


class Exam(models.Model):
    EDIT_CHOICES = ((True, 'Yes'),(False, 'No'))
    TERM_CHOICES = (("Term 1","Term 1"),("Term 2","Term 2"),("Term 3","Term 3"))
    name=models.CharField(max_length=255,null=False,unique=True)
    form = models.ManyToManyField("Form", related_name="exams")
    term = models.CharField(choices=TERM_CHOICES,default="Term 1",null=False,max_length=255)
    editable = models.BooleanField(choices=EDIT_CHOICES ,default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} {} {}".format(self.name,self.term,self.created_at.strftime("%Y"))


class Records(models.Model):
    exam =  models.ForeignKey("Exam", on_delete=models.CASCADE,related_name="records",null=False)
    student = models.ForeignKey("Student", on_delete=models.CASCADE,related_name="record",null=False)
    subject = models.ForeignKey("Subjects", on_delete=models.PROTECT,related_name="subject_records",null=False)
    score = models.PositiveIntegerField(null=False)

    def __str__(self):
        return "{} {}".format(self.exam,self.student)
    class Meta:
        verbose_name_plural="Records"