from django.db import models
from gestor.models import Gestor

class ClassificacaoPrioridade(models.Model):
    id_classificacao_prioridade = models.AutoField(primary_key=True)
    desc_classificacao_prioridade = models.CharField(max_length=150)

    def __str__(self):
        return self.desc_classificacao_prioridade

class Prioridade(models.Model):
    id_prioridade = models.AutoField(primary_key=True)
    gestor = models.ForeignKey(Gestor, on_delete=models.SET_NULL, null=True)
    classificacao_prioridade = models.ForeignKey(ClassificacaoPrioridade, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'Prioridade - {self.classificacao_prioridade}'