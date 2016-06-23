from django.conf.urls import url
from contact.views import MessageListView, MessageDetailView, MessageCreateView, \
MessageUpdateView, MessageDeleteView


urlpatterns = [
    url(r'^$', MessageListView.as_view(), name="message_list"),
    url(r'^create/$',
        MessageCreateView.as_view(),
        name="message_create"),
    url(r'^(?P<slug>[\w-]+)/$',
        MessageDetailView.as_view(),
        name="message_detail"),
    url(r'^(?P<slug>[\w-]+)/update/(?P<pk>[0-9]+)/$',
        MessageUpdateView.as_view(),
        name="message_update"),
    url(r'^(?P<slug>[\w-]+)/delete/(?P<pk>[0-9]+)/$',
        MessageDeleteView.as_view(),
        name="message_delete"),
]
