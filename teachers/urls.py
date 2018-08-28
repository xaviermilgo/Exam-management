from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^api-get-teacher$',views.get_teacher,name='get-teacher'),
    url(r'^api-post-selected-exam$',views.GetRecordsView.as_view(),name='get-selected-records'),
    url(r'^api-post-new-record$',views.saveNewRecord.as_view(),name='save-record'),
]
