from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMessage
from django.core.mail.backends.smtp import EmailBackend

from .models import (
    Relatorio,
    RelatorioImagem,
    DestinatarioEmail,
    UserSMTPConfig,
)
from .forms import (
    RelatorioForm,
    DestinatarioEmailForm,
    UserSMTPConfigForm,
)
import smtplib, ssl

# ------------------------------------------------------------------
# Utilitário simples para testar conexão SMTP (TLS porta 587)
# ------------------------------------------------------------------
def smtp_test(cfg: UserSMTPConfig):
    context = ssl.create_default_context()
    server = smtplib.SMTP(cfg.smtp_host, cfg.smtp_port, timeout=10)
    try:
        server.starttls(context=context)
        server.login(cfg.smtp_email, cfg.smtp_password)
    finally:
        server.quit()

def build_backend(cfg: UserSMTPConfig):
    """EmailBackend com TLS (porta 587)."""
    return EmailBackend(
        host=cfg.smtp_host,
        port=cfg.smtp_port,
        username=cfg.smtp_email,
        password=cfg.smtp_password,
        use_tls=True,
        fail_silently=False,
        timeout=20,
    )

# ------------------------------------------------------------------
# Páginas principais
# ------------------------------------------------------------------
@login_required
def home(request):
    hoje_count = Relatorio.objects.filter(user=request.user, data__day=request.today().day).count() if hasattr(request, 'today') else 0
    ultimo_envio = Relatorio.objects.filter(user=request.user, status_envio='enviado').order_by('-id').first()
    contexto = {
        "hoje_count": hoje_count,
        "ultimo_envio_status": "OK" if ultimo_envio else "-",
    }
    return render(request, "core/home.html", contexto)

@login_required
def dashboard(request):
    rels = Relatorio.objects.filter(user=request.user)
    contexto = {
        "total": rels.count(),
        "enviados": rels.filter(status_envio='enviado').count(),
        "drops":   sum(r.forecasted_drops for r in rels),
        "cleaned": sum(r.total_cleaned     for r in rels),
    }
    return render(request, "core/dashboard.html", contexto)

# ------------------------------------------------------------------
# Relatórios
# ------------------------------------------------------------------
@login_required
def relatorio_list(request):
    relatorios = Relatorio.objects.filter(user=request.user).order_by('-data')
    return render(request, "core/relatorio_list.html", {"relatorios": relatorios})

@login_required
def relatorio_create(request):
    if request.method == 'POST':
        form = RelatorioForm(request.POST, request.FILES)
        files = request.FILES.getlist('imagens')
        if form.is_valid():
            rel = form.save(commit=False)
            rel.user = request.user
            rel.save()
            # imagens
            for f in files:
                img = RelatorioImagem.objects.create(imagem=f)
                rel.imagens.add(img)
            rel.save()
            messages.success(request, "Relatório salvo.")
            return redirect('relatorio_list')
    else:
        form = RelatorioForm()
    return render(request, "core/relatorio_form.html", {"form": form})

@login_required
def relatorio_send_email(request, pk):
    print("===> Entrou em relatorio_send_email")          # DEBUG
    rel = get_object_or_404(Relatorio, pk=pk, user=request.user)

    # 1) SMTP
    try:
        cfg = UserSMTPConfig.objects.get(user=request.user)
    except UserSMTPConfig.DoesNotExist:
        print("!!! Sem SMTP configurado")                 # DEBUG
        messages.error(request, "Configure o SMTP no Perfil.")
        return redirect('perfil')

    # 2) Destinatários
    destinatarios = list(DestinatarioEmail.objects
                         .filter(user=request.user)
                         .values_list('email', flat=True))
    if not destinatarios:
        print("!!! Sem destinatários")                    # DEBUG
        messages.error(request, "Cadastre destinatários primeiro.")
        return redirect('emails')

    # 3) Se chegou aqui vai tentar enviar
    print(">>> Tentando enviar para", destinatarios)      # DEBUG

    subject = f"Relatório de Carros - {rel.data}"
    body = f"...dados do relatório..."

    email = EmailMessage(subject, body, cfg.smtp_email, destinatarios)
    for img in rel.imagens.all():
        email.attach_file(img.imagem.path)

    try:
        with build_backend(cfg) as con:
            con.send_messages([email])
        rel.status_envio = 'enviado'
        rel.save()
        messages.success(request, "Enviado com sucesso!")
        print("+++ Enviado OK")                           # DEBUG
    except Exception as e:
        messages.error(request, f"Erro SMTP: {e}")
        print("XXX Falha SMTP:", e)                       # DEBUG

    return redirect('relatorio_list')

# ------------------------------------------------------------------
# Destinatários
# ------------------------------------------------------------------
@login_required
def emails(request):
    lista = DestinatarioEmail.objects.filter(user=request.user)
    if request.method == 'POST':
        form = DestinatarioEmailForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('emails')
    else:
        form = DestinatarioEmailForm()
    return render(request, "core/emails.html", {"lista": lista, "form": form})

@login_required
def email_delete(request, pk):
    obj = get_object_or_404(DestinatarioEmail, pk=pk, user=request.user)
    obj.delete()
    return redirect('emails')

# ------------------------------------------------------------------
# Perfil / SMTP
# ------------------------------------------------------------------
@login_required
def perfil(request):
    cfg, _ = UserSMTPConfig.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserSMTPConfigForm(request.POST, instance=cfg)
        if form.is_valid():
            form.save()
            messages.success(request, "Configurações salvas.")
            return redirect('perfil')
    else:
        form = UserSMTPConfigForm(instance=cfg)
    return render(request, "core/perfil.html", {"form": form})

@login_required
def testar_smtp(request):
    cfg = get_object_or_404(UserSMTPConfig, user=request.user)
    try:
        smtp_test(cfg)
        messages.success(request, "Conexão SMTP OK!")
    except Exception as e:
        messages.error(request, f"Erro SMTP: {e}")
    return redirect('perfil')


from django.http import JsonResponse
from django.views.decorators.http import require_GET
...
@require_GET
@login_required
def relatorio_copy(request, pk):
    rel = get_object_or_404(Relatorio, pk=pk, user=request.user)
    texto = rel.clipboard_text()          # método que já criamos no model
    return JsonResponse({"texto": texto})
