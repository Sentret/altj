from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib import admin


class CustomUser(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)


class Class(models.Model):
    name = models.CharField(max_length=3,blank= True)

    def __str__ (self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,null=True)
    _class = models.ForeignKey(Class, on_delete=models.DO_NOTHING,null=True)

    def save(self, *args, **kwargs):
        self.user.is_student = True
        self.user.save()
        super(Student, self).save(*args, **kwargs)


    def __str__(self):
        return self.user.last_name + ' '+ self.user.first_name + ' '+ str(self._class)


class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        self.user.is_teacher = True
        self.user.save()
        super(Teacher, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.last_name + ' '+ self.user.first_name


class SubjectConfig(models.Model):
    max_value = models.IntegerField(default=10)
    #значения для оценок
    excel_min_value = models.IntegerField(default=8)
    good_min_value = models.IntegerField(default=6)
    satis_min_value = models.IntegerField(default=4)

    def __str__(self):
        return str(self.subject)



class Subject(models.Model):
    name = models.CharField(max_length=20,blank=True)
    class_name = models.ForeignKey(Class, on_delete=models.DO_NOTHING,null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.DO_NOTHING,null=True)
    subject_config = models.OneToOneField(SubjectConfig, on_delete=models.DO_NOTHING, null=True,blank=True)
    
    def save(self, *args, **kwargs):
        self.subject_config = SubjectConfig.objects.create()
        super(Subject, self).save(*args, **kwargs)

    def __str__(self):
        return self.name + ' ' + str(self.class_name)

    
class Mark(models.Model):
    value = models.IntegerField()
    name = models.CharField(max_length=30, blank=True)
    date = models.DateField(auto_now_add=True)
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING,null=True)
    subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING,null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.DO_NOTHING,null=True)

    def __str__(self):
        return self.value


