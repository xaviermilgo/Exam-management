from django.conf.urls import url
from django.views.generic.base import RedirectView
from django.views.generic import TemplateView
from django.contrib.staticfiles.views import serve
from . import views,api_views


urlpatterns = [
    # url(r'^$', serve,kwargs={'path': 'front-end/index.html'}),
    # url(r'^(?!/?static/)(?!/?media/)(?P<path>.*\..*)$',
    #     RedirectView.as_view(url='/static/front-end/%(path)s', permanent=False)),
    url(r'^$', RedirectView.as_view(url='/admin')),
    url(r'^admin/select-exam$', views.select_exam,name="select-exam"),
    url(r'^admin/view-results-list$', views.results_list, name='results-view'),
    url(r'^admin/select-exam$', views.select_exam, name='select-exam'),
    url(r'^admin/select-class-form$', views.select_class_form, name='select-class-form'),
    url(r'^form-results$',views.ResultsView.as_view(),name='form-results'),
    url(r'^api-get-teacher$',api_views.get_teacher,name='get-teacher'),
    url(r'^api-post-selected-exam$',api_views.GetRecordsView.as_view(),name='api-get-selected-records'),
    url(r'^api-post-new-record$',api_views.saveNewRecord.as_view(),name='api-save-record'),
]



