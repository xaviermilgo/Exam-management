from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^api-get-teacher$',views.get_teacher,name='get-teacher'),
    url(r'^api-post-selected-exam$',views.get_selected_records,name='get-selected-records'),
]
