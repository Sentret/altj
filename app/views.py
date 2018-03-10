from .models import Subject
from .models import Mark
from .models import Class
from .models import Student
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import auth
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
import json
import datetime


def main_page(request):
  
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        #проверяем что пользователь не NONE
        if user:
            auth.login(request, user)

            if user.is_student:               
                return redirect('/student/')

            if user.is_teacher:               
                return redirect('/teacher/')
        return HttpResponse("Неверный логин или пароль")
                        
    else:       
        return render(request,'app/main.html')


@login_required
def teacher_class_list(request):
    if not request.user.is_teacher:
        return HttpResponseForbidden()
        
    teacher = request.user.teacher
    subjects = Subject.objects.filter(teacher=teacher)
    return render(request,'app/class_list.html', {'user':request.user,'subjects':subjects})


@login_required
def teacher_mark_list(request, subject, class_name, date=''):
    
    if not request.user.is_teacher:
        return HttpResponseForbidden()

    students = Student.objects.filter(_class__name=class_name)
    subj = Subject.objects.filter(name=subject, class_name=students[0]._class)[0]



    if(date !=''):
        query = Mark.objects.filter(teacher=request.user.teacher, subject__name = subject,date__range = [date,date])
    else:
        date = datetime.date.today()
        query = Mark.objects.filter(teacher=request.user.teacher, subject__name = subject,date= date)
 
    print(date)
    marks = {}

    # группирует вот так {'John Doe': {'Работа на уроке': '4', 'Аттестационные работы': '5'}}
    for q in query:
        key = str(q.student.user.last_name+ ' '+ q.student.user.first_name )
        
        if key in marks:
            marks[key][q.name] = q.value

                   
        else:
            marks[key] = {}

            marks[key][q.name] = q.value


    #добавляет учеников без оценок в список
    for student in students:
        key = str(student.user.last_name + ' '+ student.user.first_name)
        if key not in marks:
            marks[key] = {}

    return render(request,'app/teacher.html', {'user':request.user,'marks':marks, 'subject':subject,'class_name':class_name, 'date':str(date)})


@login_required
def marks_api(request,subject,class_name):

    if not request.user.is_teacher:
        return HttpResponseForbidden()


    data = json.loads(request.body)
    date = data['date']
    marks = Mark.objects.filter(subject__name=subject, subject__class_name__name=class_name, date__range = [date,date]) 
    data.pop('date',None)


    #проходимся по полученному json и сохраняем изменения в бд
    for student, mark in data.items():
        student_name = student.split(' ')
        student_user = Student.objects.filter(user__first_name=student_name[1], user__last_name=student_name[0])[0]
        subj = Subject.objects.filter(class_name__name=student_user._class.name, name = subject)[0]
        
        student_marks = marks.filter(student=student_user)
        
        #редактирования существующих оценок
        for m in student_marks:
            m.value = mark.get(m.name,'')
            m.save()
            mark.pop(m.name, None)

        #оценка новая
        for key, value in mark.items():
            if value !='':
                new_mark = Mark.objects.create(value=value, name=key,student=student_user, subject=subj,teacher = request.user.teacher)
                new_mark.date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
                new_mark.save()
            
    return HttpResponse('OK')



@login_required
def student_main_view(request, subject_name=''):
    
    if not request.user.is_student:
        return HttpResponseForbidden()

    student = request.user.student
    _class = student._class
    subjects = Subject.objects.filter(class_name = _class).order_by('name')

    #пользователь заходит первый раз, выбирается первый предмет из списка
    if (subject_name==''):
        subject_name = subjects[0].name

    query = Mark.objects.filter(student=student, subject__name=subject_name).order_by('date')
    
    config = 0
    marks = {}
    # группирует вот так {'YYYY-MM-DD': {'Работа на уроке': '4', 'Аттестационные работы': '5'}}
    if (len(query) > 0):
        config = subjects[0]

    for q in query:
        key = str(q.date)
        if key in marks:
            marks[key][q.name] = q.value
            
        else:
            marks[key] = {}

            marks[key][q.name] = q.value

    return render(request,'app/student.html', {'user':request.user,'subjects':subjects, 'marks':marks,'config':config})


