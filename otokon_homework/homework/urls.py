from django.conf.urls import url
from homework.views import LectureListView, HomeworkListView, HomeworkDetailView, \
AnswerSheetCreateView, AnswerSheetUpdateView, AnswerSheetDeleteView


urlpatterns = [
    url(r'^$', LectureListView.as_view(), name="lecture_list"),
    url(r'^(?P<lecture>[\w-]+)/(?P<slug>[\w-]+)/answer/create/$',
        AnswerSheetCreateView.as_view(),
        name="answer_create"),
    url(r'^(?P<lecture>[\w-]+)/(?P<homework>[\w-]+)/answer/update/(?P<pk>[0-9]+)/$',
        AnswerSheetUpdateView.as_view(),
        name="answer_update"),
    url(r'^(?P<lecture>[\w-]+)/(?P<homework>[\w-]+)/answer/delete/(?P<pk>[0-9]+)/$',
        AnswerSheetDeleteView.as_view(),
        name="answer_delete"),
    url(r'^(?P<lecture>[\w-]+)/$',
        HomeworkListView.as_view(),
        name="homework_list"),
    url(r'^(?P<lecture>[\w-]+)/(?P<slug>[\w-]+)/$',
        HomeworkDetailView.as_view(),
        name="homework_detail"),

]
