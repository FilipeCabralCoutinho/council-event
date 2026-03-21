from django.shortcuts import render
from django.http import HttpResponse

def home():
    return HttpResponse("Adicione aqui a página principal!")

def new_enrollment():
    return HttpResponse("Adicione aqui o formulário de inscrição!")

def enrollment_received():
    return HttpResponse("Adicione aqui a página Inscrição Recebida!")
