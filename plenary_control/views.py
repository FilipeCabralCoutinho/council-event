from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Participante
import json


def dashboard(request):
    """Renderiza o dashboard de participantes"""
    return render(request, 'plenary_control/dashboard_participantes.html')


@require_http_methods(["GET"])
def get_participantes(request):
    """Retorna lista de participantes em JSON com estatísticas"""
    participantes = Participante.objects.all().values(
        'id_participante',
        'id_inscricao',
        'nome',
        'funcao',
        'distrito',
        'igreja',
        'no_plenario'
    )
    
    total = participantes.count()
    no_plenario = participantes.filter(no_plenario=True).count()
    fora_plenario = total - no_plenario
    percentual = (no_plenario / total * 100) if total > 0 else 0
    
    return JsonResponse({
        'participantes': list(participantes),
        'stats': {
            'total': total,
            'no_plenario': no_plenario,
            'fora_plenario': fora_plenario,
            'percentual': round(percentual, 2)
        }
    })


@require_http_methods(["GET"])
def buscar_participantes(request):
    """Busca participantes por nome ou id_participante"""
    termo = request.GET.get('q', '').strip()
    
    if not termo:
        participantes = Participante.objects.all()
    else:
        from django.db.models import Q
        participantes = Participante.objects.filter(
            Q(nome__icontains=termo) |
            Q(id_participante__icontains=termo)
        )
    
    data = participantes.values(
        'id_participante',
        'id_inscricao',
        'nome',
        'funcao',
        'distrito',
        'igreja',
        'no_plenario'
    )
    
    return JsonResponse({
        'participantes': list(data),
        'total': participantes.count()
    })


@require_http_methods(["POST"])
def atualizar_plenario(request):
    """Atualiza o status no_plenario de um participante"""
    try:
        data = json.loads(request.body)
        id_participante = data.get('id_participante')
        no_plenario = data.get('no_plenario')
        
        if id_participante is None or no_plenario is None:
            return JsonResponse(
                {'error': 'Parâmetros inválidos'},
                status=400
            )
        
        participante = Participante.objects.get(id_participante=id_participante)
        participante.no_plenario = no_plenario
        participante.save()
        
        # Recalcular estatísticas
        total = Participante.objects.count()
        plenario_count = Participante.objects.filter(no_plenario=True).count()
        fora_plenario = total - plenario_count
        percentual = (plenario_count / total * 100) if total > 0 else 0
        
        return JsonResponse({
            'success': True,
            'message': 'Participante atualizado com sucesso',
            'stats': {
                'total': total,
                'no_plenario': plenario_count,
                'fora_plenario': fora_plenario,
                'percentual': round(percentual, 2)
            }
        })
    except Participante.DoesNotExist:
        return JsonResponse(
            {'error': 'Participante não encontrado'},
            status=404
        )
    except json.JSONDecodeError:
        return JsonResponse(
            {'error': 'JSON inválido'},
            status=400
        )
    except Exception as e:
        return JsonResponse(
            {'error': str(e)},
            status=500
        )


def home(request):
    return render(request, 'plenary_control/dashboard_participantes.html')
