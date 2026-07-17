from django import forms
from .models import Inscricoes, Igreja
from django.utils.safestring import mark_safe
from .logging import logger
from datetime import datetime


class InscricaoForm(forms.ModelForm):
    # Recriar o campo pernoite sem opção vazia
    pernoite = forms.ChoiceField(
        choices=[("NAO", "NÃO"), ("SIM", "SIM")],
        widget=forms.RadioSelect(),
        initial="NAO",
        required=True,
        label="Você dormirá no acampamento Efraim?"
    )

    # Customizar possui_comorbidade para usar RadioSelect
    possui_comorbidade = forms.ChoiceField(
        choices=[("NAO", "NÃO"), ("SIM", "SIM")],
        widget=forms.RadioSelect(),
        required=True,
        label="Possui alguma Comorbidade?"
    )

    class Meta:
        model = Inscricoes
        fields = ['nome','cpf','email','whatsapp','distrito','igreja','funcao','apto_concilio','possui_comorbidade','qual_comorbidade', 'pernoite', 'quantidade_parcelas', 'consent_given']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # consentimento obrigatório
        self.fields['consent_given'].required = True
        self.fields['consent_given'].label = mark_safe(
            'Concordo com o tratamento dos meus dados pessoais para a organização deste evento, '
            'conforme a <a href="https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm" target="_blank" rel="noopener noreferrer">Lei Geral de Proteção de Dados (LGPD)</a>.'
        )
        self.fields['consent_given'].error_messages = {
            'required': 'Você precisa aceitar os termos para prosseguir.'
        }

        # diminuição progressiva da quantidade de parcelas
        range_parcelas = range(1,7)
        if datetime.now() > datetime.strptime("18/05/2026", "%d/%m/%Y"):
            range_parcelas = range(1,6)
        elif datetime.now() > datetime.strptime("18/06/2026", "%d/%m/%Y"):
            range_parcelas = range(1,5)
        elif datetime.now() > datetime.strptime("18/07/2026", "%d/%m/%Y"):
            range_parcelas = range(1,4)
        elif datetime.now() > datetime.strptime("18/08/2026", "%d/%m/%Y"):
            range_parcelas = range(1,3)
        elif datetime.now() > datetime.strptime("18/09/2026", "%d/%m/%Y"):
            range_parcelas = range(1,2)
        elif datetime.now() > datetime.strptime("18/10/2026", "%d/%m/%Y"):
            range_parcelas = range(1,1)

        # Opções de parcelas
        self.fields['quantidade_parcelas'].widget = forms.Select(
            choices=[(i, f'{i}x') for i in range_parcelas]
        )

        # Adicionar help_text ao campo apto_concilio
        text_apto = """
                    Das Atribuições do Concílio Regional Art. 50, inciso V, alíneas "a" e "b".

                    a) No ato da inscrição para o Concílio Regional, todos(as) os(as) delegados(as) deverão manifestar, de forma expressa, se desejam ou não concorrer à composição da delegação que representará a Região no Concílio Geral.

                    b) Os clérigos e leigos, só poderão concorrer para a delegação ao Concílio-Geral se estiverem em dia com suas as obrigações locais, distritais, regionais e gerais.

                    Manifesta interesse em concorrer e, caso eleito(a), integrar a delegação da VI Região no Concílio Geral de 2027?
                    """
        self.fields['apto_concilio'].help_text = mark_safe(text_apto.strip().replace('\n', '<br>'))

        # Start empty
        self.fields['igreja'].queryset = Igreja.objects.none()

        # Open option when 'distrito' selected
        if 'distrito' in self.data:
            try:
                distrito_id = int(self.data.get('distrito'))
                self.fields['igreja'].queryset = Igreja.objects.filter(distrito_id=distrito_id).order_by('nome')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['igreja'].queryset = self.instance.distrito.igreja_set.order_by('nome')

    def clean_qual_comorbidade(self):
        """Validar qual_comorbidade baseado em possui_comorbidade"""
        qual_comorbidade = self.cleaned_data.get('qual_comorbidade')
        possui_comorbidade = self.cleaned_data.get('possui_comorbidade')

        if possui_comorbidade == 'SIM' and not qual_comorbidade:
            logger.warning("Form validation failed: Comorbidity marked as YES, but not specified.")
            raise forms.ValidationError(
                'Por favor, especifique qual comorbidade você possui.'
            )

        return qual_comorbidade

    def clean(self):
        cleaned_data = super().clean()
        distrito = cleaned_data.get('distrito')
        pernoite = cleaned_data.get('pernoite')

        # Distritos que não podem ter pernoite
        distritos_sem_pernoite = ['São João de Meriti', 'Queimados', 'Nova Iguaçu', 'Nilópolis', 'Mesquita']

        if distrito and pernoite == 'SIM' and distrito.nome in distritos_sem_pernoite:
            logger.warning(f"Form validation failed: Enrollment attempt with overnight stay for restricted district ({distrito.nome}).")
            raise forms.ValidationError(
                f'Pessoas do distrito {distrito.nome} não podem se inscrever com pernoite.'
            )

        return cleaned_data
