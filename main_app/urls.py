from django.urls import path
from . import views

urlpatterns = [
    path('', views.form),
    path('registered', views.registered),
    path('logout', views.logout),
    path('login', views.login),
    path('homepage', views.homepage),
    path('add_org', views.add_org),
    path('org/<int:org_id>', views.org_info),
    path('org/<int:org_id>/delete', views.delete_org),
    path('org/<int:org_id>/join', views.join_org),
    path('org/<int:org_id>/leave', views.leave_org),
]