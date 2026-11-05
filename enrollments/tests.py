from io import BytesIO

from django.test import TestCase
from openpyxl import load_workbook

from .forms import InscricaoForm
from .models import Distrito, Igreja, Inscricoes, Pagamento, Parcela
from .services import Services


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

    def test_export_to_excel_colore_celula_falta_pagar(self):
        inscritos = []
        for index, (cpf, total_pago, esperado) in enumerate([
            ('11111111111', 630, 'verde'),
            ('22222222222', 0, 'vermelha'),
            ('33333333333', 200, 'azul'),
        ], start=1):
            inscricao = Inscricoes.objects.create(
                nome=f'Participante {index}',
                cpf=cpf,
                email=f'{cpf}@teste.com',
                whatsapp='21999999999',
                distrito=self.distrito,
                igreja=self.igreja,
                sexo='MASCULINO',
                funcao='MEMBRO',
                quantidade_parcelas=1,
                apto_concilio='SIM',
                possui_comorbidade='NAO',
                pernoite='NAO',
                consent_given=True,
            )
            inscritos.append((inscricao, total_pago, esperado))

            pagamento = Pagamento.objects.create(inscricao=inscricao, valor_total=630)
            if total_pago:
                Parcela.objects.create(pagamento=pagamento, numero=1, valor=total_pago, status='PAGA')

        response = Services.export_to_excel(Inscricoes.objects.all())

        workbook = load_workbook(filename=BytesIO(response.content))
        worksheet = workbook['Inscritos']
        header = [cell.value for cell in worksheet[1]]
        falta_pagar_index = header.index('Falta Pagar') + 1
        valor_total_index = header.index('Valor Total') + 1

        for row_number, (_, total_pago, esperado) in enumerate([('x', 630, 'verde'), ('x', 0, 'vermelha'), ('x', 200, 'azul')], start=2):
            falta_pagar = worksheet.cell(row=row_number, column=falta_pagar_index)
            valor_total = worksheet.cell(row=row_number, column=valor_total_index)

            self.assertEqual(valor_total.value, 630)
            if esperado == 'verde':
                self.assertEqual(falta_pagar.fill.fgColor.rgb.upper(), '00C6EFCE')
            elif esperado == 'vermelha':
                self.assertEqual(falta_pagar.fill.fgColor.rgb.upper(), '00F4CCCC')
            else:
                self.assertEqual(falta_pagar.fill.fgColor.rgb.upper(), '00CFE2F3')
