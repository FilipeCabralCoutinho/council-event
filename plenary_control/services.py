from ..enrollments.models import Inscricoes

def get_all_confirmed_enrollments():
    return Inscricoes.objects.filter(status_pagamento='CONFIRMADO')