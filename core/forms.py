from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import (
    Relatorio,
    DestinatarioEmail,
    UserSMTPConfig,
)

# ──────────────────────────  LOGIN  ──────────────────────────
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control form-control-sm",
            "placeholder": "E-mail"
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control form-control-sm",
            "placeholder": "Senha"
        })
    )

# ─────────────────────  RELATÓRIO DIÁRIO  ────────────────────
class RelatorioForm(forms.ModelForm):
    class Meta:
        model = Relatorio
        fields = [
            'ready_line','vip_line','overflow_kiosk','overflow_2',
            'black_top','return_line','mecanico','gas_run',
            'total_cleaned','forecasted_drops'
        ]
        widgets = {
            f: forms.TextInput(attrs={"class": "form-control form-control-sm"})
            for f in fields
        }

# ─────────────────────  DESTINATÁRIOS E-MAIL  ─────────────────
class DestinatarioEmailForm(forms.ModelForm):
    class Meta:
        model = DestinatarioEmail
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                "class": "form-control form-control-sm",
                "placeholder": "exemplo@empresa.com"
            })
        }

# ─────────────────────  CONFIG. SMTP (TLS)  ───────────────────
class UserSMTPConfigForm(forms.ModelForm):
    smtp_password = forms.CharField(
        required=False,                       # pode vir vazio para manter
        widget=forms.PasswordInput(
            attrs={"class":"form-control form-control-sm"},
            render_value=True                 # mostra **** ao reabrir
        )
    )

    class Meta:
        model = UserSMTPConfig
        fields = ['smtp_email','smtp_password','smtp_host','smtp_port']
        widgets = {
            'smtp_email': forms.EmailInput(attrs={"class":"form-control form-control-sm"}),
            'smtp_host':  forms.TextInput(attrs={"class":"form-control form-control-sm"}),
            'smtp_port':  forms.NumberInput(attrs={"class":"form-control form-control-sm"}),
        }

    def save(self, commit=True):
        """Se senha vier vazia, mantém a anterior."""
        instance = super().save(commit=False)
        if not self.cleaned_data.get("smtp_password"):
            instance.smtp_password = self.instance.smtp_password
        if commit:
            instance.save()
        return instance
