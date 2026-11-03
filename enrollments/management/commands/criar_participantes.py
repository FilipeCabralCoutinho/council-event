"""Script que serve para criar Participantes ainda não criados para todas as Inscrições existentes."""

from django.core.management.base import BaseCommand
from plenary_control.services import PlenaryService

plenary_service = PlenaryService()


class Command(BaseCommand):
    help = 'Cadastra os participantes no banco de dados com base nas inscrições existentes'

    def handle(self, *args, **options):
        try:
            plenary_service.create_all_participants()

            self.stdout.write(self.style.SUCCESS("\n--- Resumo ---"))
            self.stdout.write(self.style.SUCCESS("Participantes Atualizados de acordo com as Inscrições existentes"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"✗ Erro ao criar participantes: {str(e)}"))

## Command to execute: python3 manage.py criar_participantes
