from django.contrib import admin
from .models import Class,Form,Subjects,TeacherRoles,Student,Exam,Streams,Records,Teacher,Grades,OverallGrade

admin.site.register(
    Exam,
    list_display=["name","term","created_at","editable"],
    search_fields=["name","term"],

)
admin.site.register(
    Student,
    list_display=["admno","name","class_name"],
    search_fields = ["admno","name","class_name__stream__name"]
)
admin.site.register(
    Teacher,
    list_display=["user","phone_number"],
    search_fields = ["phone_number","user__username"],
)
admin.site.register(
    TeacherRoles,
    list_display=["teacher","class_name","subject"],
    search_fields=["teacher__user__username","class_name__stream__name","subject__name"]

)
admin.site.register(
    Class,
    list_display=["form","stream"],
    search_fields=["form__name","stream__name"]

)
admin.site.register(
    Form,
    search_fields=["name"],
)
admin.site.register(
    Streams,
    search_fields=["name"],
)

admin.site.register(
    Subjects,
    list_display=["abbreviation","name","compulsory"],
    search_fields=["abbreviation","name"],
)

admin.site.register(
    Grades,
    list_display=["name","low_score","high_score","points"],
    search_fields=["name","low_score","high_score","points"]

)
admin.site.register(
    OverallGrade,
    list_display=["name","low_points","high_points"],
    search_fields=["name","low_points","high_points"],
)
