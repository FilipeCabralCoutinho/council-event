from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from .forms import EnrollmentForm

def home(request):
    return HttpResponse("Adicione aqui a página principal!")

def new_enrollment(request:HttpRequest):
    if request.method == "POST":
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("enrollments:enrollment_received")

    context = {
        "form": EnrollmentForm
    }
    return render(request, 'enrollments/new_enrollment.html', context)

def enrollment_received(request):
    return HttpResponse("Adicione aqui a página Inscrição Recebida!")
