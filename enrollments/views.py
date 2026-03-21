from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("Adicione aqui a página principal!")

def new_enrollment(request):
    return HttpResponse("Adicione aqui o formulário de inscrição!")

def enrollment_received(request):
    return HttpResponse("Adicione aqui a página Inscrição Recebida!")
