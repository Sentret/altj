from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import Student
from .models import Teacher
from .models import Subject
from .models import Class
from .models import Mark

admin.site.register(CustomUser,UserAdmin)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(Class)
admin.site.register(Mark)