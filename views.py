from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from .models import Student

@login_required
def home(request):
    query = request.GET.get('search')
    if query:
        students = Student.objects.filter(full_name__icontains=query)
    else:
        students = Student.objects.all()
    return render(request, 'students/index.html', {'students': students})

@login_required
def add_student(request):
    if request.method == "POST":
        roll = request.POST.get('roll')
        name = request.POST.get('name')
        course = request.POST.get('course')
        Student.objects.create(roll_no=roll, full_name=name, course=course)
        messages.success(request, f'Student {name} added successfully!')
        return redirect('home')
    return render(request, 'students/add_student.html')

@login_required
def edit_student(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == "POST":
        student.roll_no = request.POST.get('roll')
        student.full_name = request.POST.get('name')
        student.course = request.POST.get('course')
        student.save()
        messages.info(request, f'Details for {student.full_name} updated!')
        return redirect('home')
    return render(request, 'students/edit_student.html', {'student': student})

@login_required
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    name = student.full_name
    student.delete()
    messages.warning(request, f'Student {name} deleted.')
    return redirect('home')

def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')