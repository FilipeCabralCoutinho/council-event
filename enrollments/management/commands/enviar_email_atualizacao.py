from django.core.management.base import BaseCommand
from enrollments.models import Inscricoes
from enrollments.services import Services
import time

services = Services()
_INTERVAL_TO_SEND_EMAILS = 5  # Intervalo em segundos entre o envio de cada e-mail


class Command(BaseCommand):
    help = 'Envia e-mails de atualização para os inscritos'

    def handle(self, *args, **options):
        fail = 0
        success = 0

        enrollments = Inscricoes.objects.all()
        for enrollment in enrollments:
            if enrollment.email:
                try:
                    services.send_email(enrollment, 'update_payment_email')
                    self.stdout.write(self.style.SUCCESS(f'E-mail enviado para {enrollment.email}'))

                    success += 1
                    time.sleep(_INTERVAL_TO_SEND_EMAILS)  # Aguarda o intervalo definido antes de enviar o próximo e-mail

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Erro ao enviar e-mail para {enrollment.email}: {str(e)}'))
                    fail += 1
                    time.sleep(_INTERVAL_TO_SEND_EMAILS)  # Aguarda o intervalo definido antes de enviar o próximo e-mail

        self.stdout.write(self.style.SUCCESS(f'Lista de e-mails finalizada. (Sucesso: {success}, Falha: {fail})'))

## Command to execute: python3 manage.py enviar_email_atualizacao