from django.core.management.base import BaseCommand
from enrollments.models import Distrito

class Command(BaseCommand):
    help = 'Cadastra os distritos no banco de dados'

    def handle(self, *args, **options):
        distritos = [
            "Agulhas Negras",
            "Bangu",
            "Barra do Piraí",
            "Barra Mansa",
            "Campo Grande",
            "Costa Verde",
            "Grajaú",
            "Jacarepaguá",
            "Maranhão",
            "Mesquita",
            "Nilópolis",
            "Nova Iguaçu",
            "Piraí",
            "Queimados",
            "Retiro",
            "Sta. Margarida",
            "São João de Meriti",
            "Volta Redonda"
        ]

        for nome in distritos:
            distrito, criado = Distrito.objects.get_or_create(nome=nome)
            status = "Criado" if criado else "Já existia"
            self.stdout.write(f"✓ {status}: {nome}")

        self.stdout.write(self.style.SUCCESS(f"\nTotal: {Distrito.objects.count()}"))

## Comand to execute: python3 manage.py cadastrar_distritos
