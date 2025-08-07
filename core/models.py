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

    def clipboard_text(self) -> str:
        """Texto pronto para copiar/colar no e-mail ou chat."""
        return (
            f"Below the cars count of {self.data.strftime('%d/%m/%y')}\n\n"
            f"ready line =  {self.ready_line}\n\n"
            f"VIP line = {self.vip_line}\n\n"
            f"Overflow Kiosk = {self.overflow_kiosk}\n"
            f"Overflow 2 = {self.overflow_2}\n\n"
            f"Black top = {self.black_top}\n\n"
            f"return = {self.return_line}\n"
            f"Mecânico = {self.mecanico}\n"
            f"gas run = {self.gas_run}\n\n"
            f"Total count of cleaned cars: {self.total_cleaned}\n\n"
            f"Forecasted drops: {self.forecasted_drops}\n"
        )

class UserSMTPConfig(models.Model):
    user          = models.OneToOneField(User, on_delete=models.CASCADE)
    smtp_email    = models.EmailField()
    smtp_password = models.CharField(max_length=128)
    # TLS fixo – valores padrão do Outlook; se quiser outro provedor o usuário só troca.
    smtp_host     = models.CharField(max_length=128, default='smtp.office365.com')
    smtp_port     = models.PositiveIntegerField(default=587)

    def __str__(self):
        return f"{self.smtp_email} ({self.smtp_host}:{self.smtp_port})"
