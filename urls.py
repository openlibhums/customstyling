from django.conf.urls import url

from plugins.customstyling import views


urlpatterns = [
    url(r'^manager/$', views.manager, name='customstyling_manager'),
    url(r'^manager/press/$', views.manage_press_css, name='customstyling_manage_press_css'),
    url(r'^manager/journal/(?P<journal_id>\d+)$', views.manage_css, name='customstyling_manage_css'),

    url(r'^manager/cjs/new/$', views.manage_cross_journal_stylesheets, name='customstyling_new_lcjsc'),
    url(r'^manager/cjs/(?P<stylesheet_id>\d+)/$', views.manage_cross_journal_stylesheets, name='customstyling_edit_lcjsc'),
]
