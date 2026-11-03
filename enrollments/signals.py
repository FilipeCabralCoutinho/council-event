from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Inscricoes
from .services import Services as EnrollmentService
from plenary_control.services import PlenaryService

enrollment_service = EnrollmentService()
plenary_service = PlenaryService()

@receiver(pre_save, sender=Inscricoes)
def send_payment_confirmation_email(sender, instance, **kwargs):
    """
    Envia email de confirmação de pagamento quando o status_pagamento
    muda de 'PENDENTE' para 'CONFIRMADO'
    """
    # Ignora criações novas (apenas updates)
    if not instance.pk:
        return

    try:
        # Obtém a instância anterior do banco de dados (antes de qualquer mudança)
        old_instance = Inscricoes.objects.get(pk=instance.pk)
    except Inscricoes.DoesNotExist:
        return

    # Verifica se o status mudou de PENDENTE para CONFIRMADO
    if (old_instance.status_pagamento == 'PENDENTE' and
        instance.status_pagamento == 'CONFIRMADO'):

        # Marca para enviar email após salvar (será enviado no post_save)
        instance._send_payment_email = True


@receiver(post_save, sender=Inscricoes)
def trigger_payment_email(sender, instance, created, **kwargs):
    """
    Dispara o envio de email após o modelo ser salvo
    """
    if created:
        return

    if hasattr(instance, '_send_payment_email') and instance._send_payment_email:
        enrollment_service.send_email(instance, email_type='payment_confirmation')


@receiver(post_save, sender=Inscricoes)
def create_participant_when_enrollment_created(sender, instance, created, **kwargs):
    """
    Cria um participante quando a inscrição é criada.
    """
    if created:
        plenary_service.create_participant(instance.id)
