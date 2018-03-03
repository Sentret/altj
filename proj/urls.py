from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main_page, name='main_page'),
    path('teacher/', views.teacher_class_list),
    path('marks_api/<subject>/<class_name>/', views.marks_api),
    path('teacher/<subject>/<class_name>/',views.teacher_mark_list),
    path('teacher/<subject>/<class_name>/<date>',views.teacher_mark_list),
    path('student/', views.student_main_view),
    path('student/<subject>/', views.student_main_view),
]
