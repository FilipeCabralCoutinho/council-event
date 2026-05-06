import json
import io
import pandas as pd
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, HttpRequest, JsonResponse, FileResponse
from .forms import InscricaoForm
from .models import Igreja, Inscricoes, Distrito
from .services import Services
from django.conf import settings
from django.db.models import Count
from django.contrib.admin.views.decorators import staff_member_required
from .logging import logger

service = Services()


def get_client_ip(request):
    """
    Extrai o IP do cliente do request,
    considerando proxies reversos
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def home(request):
    logger.info("Main page (home) accessed.")
    return render(request, 'enrollments/home.html')

def new_enrollment(request:HttpRequest):
    if request.method == "POST":
        form = InscricaoForm(request.POST)
        cpf = request.POST.get("cpf")
        logger.info(f"New enrollment attempt. CPF: {cpf}, IP: {get_client_ip(request)}")

        if form.is_valid():
            enrollment = form.save(commit=False)
            enrollment.ip_address = get_client_ip(request)
            enrollment.save()

            enrollment = Inscricoes.objects.get(cpf=cpf)
            logger.info(f"Enrollment successfully saved. ID: {enrollment.id}, CPF: {cpf}")

            service.payment(enrollment.id)
            service.send_email(enrollment)

            return redirect("enrollments:enrollment_received")
        else:
            logger.warning(f"Form validation failed. CPF: {cpf}. Errors: {form.errors}")
            messages.error(request, "Formulário inválido! Verifique os dados e tente novamente.")
            if Inscricoes.objects.filter(cpf=cpf).exists():
                logger.warning(f"Enrollment attempt with already registered CPF: {cpf}")
                messages.error(request, "CPF JÁ CADASTRADO!")
            return redirect('enrollments:new_enrollment')




    # Distritos que não têm opção de pernoite
    distritos_sem_pernoite = [
        'São João de Meriti',
        'Queimados',
        'Nova Iguaçu',
        'Nilópolis',
        'Mesquita'
    ]

    context = {
        "form": InscricaoForm,
        "distritos_sem_pernoite": distritos_sem_pernoite
    }
    return render(request, 'enrollments/new_enrollment.html', context)

def enrollment_received(request):
    logger.info("Enrollment confirmation page accessed.")
    context = {
        "PIX_KEY": settings.PIX_KEY
    }
    return render(request, 'enrollments/enrollment_received.html', context)

def busca_igrejas_por_distrito(request):
    distrito_id = request.GET.get('distrito_id')
    logger.info(f"AJAX search for churches requested for distrito_id: {distrito_id}")
    
    # Filtra as igrejas baseadas no ID do distrito recebido
    igrejas = Igreja.objects.filter(distrito_id=distrito_id).values('id', 'nome').order_by('nome')
    return JsonResponse(list(igrejas), safe=False)

def export_file(request, file):
    return FileResponse(file, as_attachment=True, filename="Inscrições")

@staff_member_required
def dashboard(request):
    logger.info(f"Dashboard accessed by user: {request.user}")
    # 1. Totais Gerais
    total_inscricoes = Inscricoes.objects.count()
    
    # 2. Status de Pagamento
    total_pendente = Inscricoes.objects.filter(status_pagamento='PENDENTE').count()
    total_confirmado = Inscricoes.objects.filter(status_pagamento='CONFIRMADO').count()
    
    # 3. Pernoite
    total_com_pernoite = Inscricoes.objects.filter(pernoite='SIM').count()
    total_sem_pernoite = Inscricoes.objects.filter(pernoite='NAO').count()
    
    # 4. Total por Distrito
    distritos_stats = Distrito.objects.annotate(
        total_inscricoes=Count('inscricoes')
    ).filter(total_inscricoes__gt=0).order_by('-total_inscricoes')
    
    # 5. Dados das Igrejas por Distrito (para o dropdown via JS)
    igrejas_stats = Igreja.objects.annotate(
        total_inscricoes=Count('inscricoes')
    ).filter(total_inscricoes__gt=0).values('distrito_id', 'nome', 'total_inscricoes')
    
    igrejas_por_distrito = {}
    for igreja in igrejas_stats:
        distrito_id = str(igreja['distrito_id'])
        if distrito_id not in igrejas_por_distrito:
            igrejas_por_distrito[distrito_id] = []
        igrejas_por_distrito[distrito_id].append({
            'nome': igreja['nome'],
            'total': igreja['total_inscricoes']
        })

    context = {
        'total_inscricoes': total_inscricoes,
        'total_pendente': total_pendente,
        'total_confirmado': total_confirmado,
        'total_com_pernoite': total_com_pernoite,
        'total_sem_pernoite': total_sem_pernoite,
        'distritos_stats': distritos_stats,
        'igrejas_por_distrito_json': json.dumps(igrejas_por_distrito),
        'distritos': Distrito.objects.all().order_by('nome'),
    }
    return render(request, 'enrollments/dashboard.html', context)

@staff_member_required
def export_dashboard_excel(request):
    logger.info(f"Dashboard statistics export to Excel requested by user: {request.user}")
    # 1. Totais Gerais
    df_geral = pd.DataFrame([{
        'Total Inscrições': Inscricoes.objects.count(),
        'Pagamento Pendente': Inscricoes.objects.filter(status_pagamento='PENDENTE').count(),
        'Pagamento Confirmado': Inscricoes.objects.filter(status_pagamento='CONFIRMADO').count(),
        'Com Pernoite': Inscricoes.objects.filter(pernoite='SIM').count(),
        'Sem Pernoite': Inscricoes.objects.filter(pernoite='NAO').count()
    }])

    # 2. Total por Distrito
    distritos_stats = Distrito.objects.annotate(
        total_inscricoes=Count('inscricoes')
    ).order_by('-total_inscricoes').values('nome', 'total_inscricoes')
    
    df_distritos = pd.DataFrame(list(distritos_stats))
    if not df_distritos.empty:
        df_distritos.rename(columns={'nome': 'Distrito', 'total_inscricoes': 'Total Inscrições'}, inplace=True)
    else:
        df_distritos = pd.DataFrame(columns=['Distrito', 'Total Inscrições'])

    # 3. Total por Igreja
    igrejas_stats = Igreja.objects.annotate(
        total_inscricoes=Count('inscricoes')
    ).values('distrito__nome', 'nome', 'total_inscricoes').order_by('distrito__nome', '-total_inscricoes')

    df_igrejas = pd.DataFrame(list(igrejas_stats))
    if not df_igrejas.empty:
        df_igrejas.rename(columns={'distrito__nome': 'Distrito', 'nome': 'Igreja', 'total_inscricoes': 'Total Inscrições'}, inplace=True)
    else:
        df_igrejas = pd.DataFrame(columns=['Distrito', 'Igreja', 'Total Inscrições'])

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_geral.to_excel(writer, index=False, sheet_name='Visão Geral')
        df_distritos.to_excel(writer, index=False, sheet_name='Por Distrito')
        df_igrejas.to_excel(writer, index=False, sheet_name='Por Igreja')

    output.seek(0)
    response = HttpResponse(
        output.read(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="estatisticas_concilio.xlsx"'
    return response
