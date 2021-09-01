from django.conf.urls import url

from plugins.customstyling import views


urlpatterns = [
    url(r'^manager/$', views.manager, name='customstyling_manager'),
    url(r'^manager/journal/(?P<journal_id>\d+)$', views.manage_css, name='customstyling_manage_css'),
]
