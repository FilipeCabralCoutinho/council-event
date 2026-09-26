from django.test import TestCase

from .forms import InscricaoForm
from .models import Distrito, Igreja, Inscricoes


class PernoiteCapacidadeTests(TestCase):
    def setUp(self):
        self.distrito = Distrito.objects.create(nome='Centro')
        self.igreja = Igreja.objects.create(nome='Igreja Teste', distrito=self.distrito)

    def _dados_inscricao(self, cpf, pernoite='NAO'):
        return {
            'nome': 'João da Silva',
            'sexo': 'MASCULINO',
            'cpf': cpf,
            'email': f'{cpf}@teste.com',
            'whatsapp': '21999999999',
            'distrito': self.distrito.id,
            'igreja': self.igreja.id,
            'funcao': 'MEMBRO',
            'apto_concilio': 'SIM',
            'possui_comorbidade': 'NAO',
            'pernoite': pernoite,
            'quantidade_parcelas': 1,
            'consent_given': True,
        }

    def test_form_rejeita_registro_com_pernoite_quando_capacidade_atingida(self):
        for i in range(300):
            cpf = str(i).zfill(11)
            Inscricoes.objects.create(
                nome='Participante',
                cpf=cpf,
                email=f'{cpf}@exemplo.com',
                whatsapp='21999999999',
                distrito=self.distrito,
                igreja=self.igreja,
                sexo='MASCULINO',
                funcao='MEMBRO',
                quantidade_parcelas=1,
                apto_concilio='SIM',
                possui_comorbidade='NAO',
                pernoite='SIM',
                consent_given=True,
            )

        form = InscricaoForm(data=self._dados_inscricao('30000000000', 'SIM'))

        self.assertFalse(form.is_valid())
        self.assertIn('pernoite', form.errors)
        self.assertIn('esgot', form.errors['pernoite'][0].lower())
