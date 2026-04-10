from django import forms
from .models import Inscricoes, Igreja


class InscricaoForm(forms.ModelForm):
    class Meta:
        model = Inscricoes
        fields = ['nome','cpf','email','whatsapp','distrito','igreja','funcao','apto_concilio','possui_comorbidade','qual_comorbidade', 'pernoite', 'quantidade_parcelas', 'consent_given']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # consentimento obrigatório
        self.fields['consent_given'].required = True
        self.fields['consent_given'].error_messages = {
            'required': 'Você precisa aceitar os termos para prosseguir.'
        }

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
