from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('ac_health/',views.ac_health,name="ac_health"),
    path('ac_content/',views.ac_content,name="ac_content"),
    path('ac_talk/',views.ac_talk,name="ac_talk"),
    path('handle_health/',views.handle_health,name="handle_health"),
    path('gai_health/',views.gai_health,name="gai_health"),
    path('ac_customer/',views.ac_customer,name="ac_customer"),
    path('gai_customer/',views.gai_customer,name="gai_customer"),
    path('del_customer/',views.del_customer,name="del_customer"),
    path('add_customer/',views.add_customer,name="add_customer"),
    path('cha_customer/',views.cha_customer,name="cha_customer"),
]