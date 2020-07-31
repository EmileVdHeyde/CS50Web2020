from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>/",views.title,name="title"),
    path("search/",views.search,name="search"), 
    path("addnew/",views.addnew,name="addnew"),
    path("edit/<str:name>",views.edit,name="edit"),
    path("random/",views.randomselect,name="random")    
]
