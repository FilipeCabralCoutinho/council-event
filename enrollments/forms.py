from django import forms
from .models import Inscricoes, Igreja
from django.utils.safestring import mark_safe
from .logging import logger


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

        # Opções de parcelas
        self.fields['quantidade_parcelas'].widget = forms.Select(
            choices=[(i, f'{i}x') for i in range(1, 9)]
        )

        # Adicionar help_text ao campo apto_concilio
        self.fields['apto_concilio'].help_text = '(Conhece o Estatuto e Regimento interno da denominação? Tem Disponibilidade para viajar?)'

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
