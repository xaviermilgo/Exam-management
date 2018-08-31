from django.db import models
from django.contrib.auth.models import User
import datetime
from django.contrib.postgres.fields import JSONField

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    phone_number=  models.CharField(max_length=10,null=False,unique=True)
    def __str__(self):
        return "{} {}".format(self.user,self.phone_number)


class TeacherRoles(models.Model):
    teacher = models.ForeignKey("Teacher", on_delete=models.CASCADE, null=False,related_name="roles")
    subject = models.ForeignKey("Subjects", on_delete=models.PROTECT,related_name="teacher_roles")
    class_name = models.ForeignKey("Class", on_delete=models.PROTECT,related_name="role")

    class Meta:
        verbose_name_plural="Teacher Roles"
        unique_together = (("subject","class_name"),)

    def __str__(self):
        return "{} {} {}".format(self.teacher.user,self.subject,self.class_name)

class Subjects(models.Model):
    REQ_CHOICES = ((True, 'Yes'),(False, 'No'))
    name= models.CharField(max_length=255,null=False,unique=True)
    abbreviation= models.CharField(max_length=4,null=False,unique=True)
    # form = models.ManyToManyField("Form",related_name="form_subjects")
    compulsory=models.BooleanField(choices=REQ_CHOICES ,default=False)

    class Meta:
        verbose_name_plural="Subjects"

    def __str__(self):
        return str(self.name)

class Form(models.Model):
    name = models.CharField(max_length=255,null=False,unique=True)
    minimum_subjects = models.PositiveIntegerField(null=False,default=1)

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
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.admno)


class Exam(models.Model):
    EDIT_CHOICES = ((True, 'Yes'),(False, 'No'))
    TERM_CHOICES = (("Term 1","Term 1"),("Term 2","Term 2"),("Term 3","Term 3"))
    name=models.CharField(max_length=255,null=False)
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
    grade= models.ForeignKey("Grades", on_delete=models.PROTECT,related_name="subject_records",null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return "{} {}".format(self.exam,self.student)

    def set_grade(self):
        try:
            self.grade= Grades.objects.get(high_score__gte=self.score,low_score__lte=self.score)
            return True
        except Exception as err:
            print(err)
            return False

    class Meta:
        verbose_name_plural="Records"
        unique_together = ("exam","student","subject")

    # grade a score
    # Grades.objects.get(high_score__gte=10,low_score__lte=10)

class Grades(models.Model):
    name= models.CharField(max_length=255,null=False,unique=True)
    high_score = models.PositiveIntegerField(null=False,unique=True)
    low_score = models.PositiveIntegerField(null=False,unique=True)
    points = models.PositiveIntegerField(null=False,unique=True) 

    class Meta:
        verbose_name_plural="Grades"
    def __str__(self):
        return "{}-{} {} points:{}".format(self.low_score,self.high_score,self.name,self.points)


class OverallGrade(models.Model):
    name= models.CharField(max_length=255,null=False,unique=True)
    high_points = models.DecimalField(null=False,decimal_places=2,max_digits=5)
    low_points = models.DecimalField(null=False,decimal_places=2,max_digits=5)
    class Meta:
        verbose_name_plural="Overall Grades"

    def __str__(self):
        return "{}-{} {}".format(self.low_points,self.high_points,self.name)

class Results(models.Model):
    # do not migrate if not using postgres 
    TYPES=(("form","form"),("class","class"))
    type_name=models.CharField(choices=TYPES,null=False,max_length=255)
    type_id=models.CharField(max_length=20,null=False)
    exam= models.ForeignKey("Exam", on_delete=models.PROTECT,related_name="results",null=False)
    results = JSONField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

