"""student_info URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/login/', views.login),
    path('user/class/', views.classes),
    path('user/add_class/', views.add_class),
    path('user/edit_class/', views.edit_class),
    path('user/del_class/', views.del_class),
    path('user/student/', views.student, name='student'),
    path('user/add_student/', views.add_student),
    path('user/edit_student/', views.edit_student),
    path('user/del_student/', views.del_student),
    path('user/add_class_modal/', views.add_class_modal),
    path('user/edit_class_modal/', views.edit_class_modal),
    path('user/del_class_modal/', views.del_class_modal),
    path('user/add_student_modal/', views.add_student_modal),
    path('user/edit_student_modal/', views.edit_student_modal),
    path('user/del_student_modal/', views.del_student_modal),
    path('user/teacher/', views.teacher),
    path('user/add_teacher/', views.add_teacher),
    path('user/edit_teacher/', views.edit_teacher),
    path('user/add_teacher_modal/', views.add_teacher_modal),
    path('user/del_teacher_modal/', views.del_teacher_modal),
]
