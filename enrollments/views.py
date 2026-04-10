from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, HttpRequest, JsonResponse, FileResponse
from .forms import InscricaoForm
from .models import Igreja, Inscricoes
from .services import Services

service = Services()

def home(request):
    return HttpResponse("Página principal!")

def new_enrollment(request:HttpRequest):
    if request.method == "POST":
        form = InscricaoForm(request.POST)
        cpf = request.POST.get("cpf")

        if form.is_valid():
            form.save()
            enrollment = Inscricoes.objects.get(cpf=cpf)

            service.payment(enrollment.id)

            service.send_email(enrollment)

            return redirect("enrollments:enrollment_received")
        else:
            if Inscricoes.objects.filter(cpf=cpf).exists():
                messages.error(request, "CPF JÁ CADASTRADO!")
                return redirect('enrollments:new_enrollment')


    context = {
        "form": InscricaoForm
    }
    return render(request, 'enrollments/new_enrollment.html', context)

def enrollment_received(request):
    return HttpResponse("Página Inscrição Recebida!")

def busca_igrejas_por_distrito(request):
    distrito_id = request.GET.get('distrito_id')
    # Filtra as igrejas baseadas no ID do distrito recebido
    igrejas = Igreja.objects.filter(distrito_id=distrito_id).values('id', 'nome').order_by('nome')
    return JsonResponse(list(igrejas), safe=False)

def export_file(request, file):
    return FileResponse(file, as_attachment=True, filename="Inscrições")
