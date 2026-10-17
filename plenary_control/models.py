from django.db import models


class Participante(models.Model):
    id_participante = models.AutoField(primary_key=True)
    id_inscricao = models.IntegerField(blank=False, null=False)
    nome = models.CharField(max_length=255)
    email = models.EmailField()
    whatsapp = models.CharField(max_length=20)
    cpf = models.CharField(max_length=14, unique=True)
    status_pagamento = models.CharField(max_length=20)
    distrito = models.CharField(max_length=255)
    igreja = models.CharField(max_length=255)
    funcao = models.CharField(max_length=50)
    pernoite = models.CharField(max_length=3)
    comorbidade = models.CharField(max_length=3)
    qual_comorbidade = models.CharField(max_length=255, blank=True)
    no_plenario = models.BooleanField(default=False)
    check_in = models.BooleanField(default=False)

    def __str__(self):
        return (
            f"Nr_Participante: {self.id_participante} | "
            f"Nome: {self.nome} | "
            f"Distrito: {self.distrito} | "
            f"Igreja: {self.igreja} | "
            f"No Plenário: {self.no_plenario}"
        )
