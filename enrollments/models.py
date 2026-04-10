from django.db import models


class Distrito(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True, unique=True)
    nome = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nome}"


class Igreja(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True, unique=True)
    nome = models.CharField(max_length=100)
    distrito =  models.ForeignKey(Distrito, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.nome}"


class Inscricoes(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True, unique=True)
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, verbose_name="CPF", unique=True)
    email = models.EmailField()
    whatsapp = models.CharField(max_length=11, verbose_name="Whatsapp/celular")
    distrito = models.ForeignKey(Distrito, on_delete=models.PROTECT)
    igreja = models.ForeignKey(Igreja, on_delete=models.PROTECT)
    funcao = models.CharField(choices=[("CLERIGO", "Clérigo (Pastor/Missionária)"), ("MEMBRO", "Membro")], verbose_name="Função")
    quantidade_parcelas = models.IntegerField(default=1)
    status_pagamento = models.CharField(choices=[('PENDENTE', 'PENDENTE'), ('CONFIRMADO', 'CONFIRMADO')],default='PENDENTE')
    apto_concilio = models.CharField(choices=[("NAO", "NÃO"), ("SIM", "SIM")], verbose_name="Apto para o Concílio Geral?")
    possui_comorbidade = models.CharField(choices=[("NAO", "NÃO"), ("SIM", "SIM")], verbose_name="Possui alguma Comorbidade?")
    qual_comorbidade = models.CharField(max_length=100, blank=True, verbose_name="Qual Comorbidade?")
    pernoite = models.CharField(choices=[("NAO", "NÃO"), ("SIM", "SIM")], verbose_name="Você dormirá no acampamento Efraim?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    consent_given = models.BooleanField(default=False)
    ip_address = models.CharField(blank=True)
    last_email = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.id} | Nome: {self.nome} | CPF: {self.cpf} | Status Pagamento: {self.status_pagamento}"

class Pagamento(models.Model):
    inscricao = models.OneToOneField(Inscricoes, on_delete=models.CASCADE, related_name='pagamento')
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)


class Parcela(models.Model):
    pagamento = models.ForeignKey(Pagamento, on_delete=models.CASCADE, related_name='parcelas')
    numero = models.IntegerField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    
    status = models.CharField(
        choices=[('PENDENTE', 'PENDENTE'), ('CONFIRMADO', 'CONFIRMADO')],
        default='PENDENTE'
    )
