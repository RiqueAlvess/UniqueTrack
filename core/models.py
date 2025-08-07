from django.db import models
from django.contrib.auth.models import User

class DestinatarioEmail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()

    def __str__(self):
        return self.email

class RelatorioImagem(models.Model):
    imagem = models.ImageField(upload_to='relatorios/')

class Relatorio(models.Model):
    STATUS_CHOICES = (
        ('enviado', 'Enviado'),
        ('nao_enviado', 'Não enviado'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.DateField(auto_now_add=True)
    ready_line = models.CharField(max_length=16)
    vip_line = models.CharField(max_length=16)
    overflow_kiosk = models.CharField(max_length=16)
    overflow_2 = models.CharField(max_length=16)
    black_top = models.CharField(max_length=16)
    return_line = models.CharField(max_length=16)
    mecanico = models.CharField(max_length=16)
    gas_run = models.CharField(max_length=16)
    total_cleaned = models.PositiveIntegerField()
    forecasted_drops = models.PositiveIntegerField()
    status_envio = models.CharField(max_length=16, choices=STATUS_CHOICES, default='nao_enviado')
    imagens = models.ManyToManyField(RelatorioImagem, blank=True)

class UserSMTPConfig(models.Model):
    user          = models.OneToOneField(User, on_delete=models.CASCADE)
    smtp_email    = models.EmailField()
    smtp_password = models.CharField(max_length=128)
    # TLS fixo – valores padrão do Outlook; se quiser outro provedor o usuário só troca.
    smtp_host     = models.CharField(max_length=128, default='smtp.office365.com')
    smtp_port     = models.PositiveIntegerField(default=587)

    def __str__(self):
        return f"{self.smtp_email} ({self.smtp_host}:{self.smtp_port})"
