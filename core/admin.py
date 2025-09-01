from django.contrib import admin
from .models import Relatorio, RelatorioImagem, DestinatarioEmail, UserSMTPConfig

# Admin customizado para UserSMTPConfig para debug
@admin.register(UserSMTPConfig)
class UserSMTPConfigAdmin(admin.ModelAdmin):
    list_display = [
        'user', 
        'smtp_email', 
        'password_status', 
        'smtp_host', 
        'smtp_port',
        'created_info'
    ]
    list_filter = ['smtp_host', 'smtp_port']
    search_fields = ['user__username', 'smtp_email']
    readonly_fields = ['password_status', 'password_length', 'created_info']
    
    fieldsets = (
        ('Usuário', {
            'fields': ('user',)
        }),
        ('Configurações de E-mail', {
            'fields': ('smtp_email', 'smtp_password', 'password_status', 'password_length')
        }),
        ('Configurações SMTP (não usadas na API)', {
            'fields': ('smtp_host', 'smtp_port'),
            'classes': ('collapse',)
        }),
        ('Debug Info', {
            'fields': ('created_info',),
            'classes': ('collapse',)
        }),
    )
    
    def password_status(self, obj):
        if obj.smtp_password:
            return f"✅ Configurada ({len(obj.smtp_password)} chars)"
        return "❌ Vazia"
    password_status.short_description = "Status da Senha"
    
    def password_length(self, obj):
        return len(obj.smtp_password) if obj.smtp_password else 0
    password_length.short_description = "Tamanho da Senha"
    
    def created_info(self, obj):
        return f"ID: {obj.id}"
    created_info.short_description = "Info"

# Admin customizado para Destinatários
@admin.register(DestinatarioEmail)
class DestinatarioEmailAdmin(admin.ModelAdmin):
    list_display = ['email', 'user']
    list_filter = ['user']
    search_fields = ['email', 'user__username']

# Admin customizado para Relatórios
@admin.register(Relatorio)
class RelatorioAdmin(admin.ModelAdmin):
    list_display = [
        'data', 
        'user', 
        'status_envio', 
        'total_cleaned', 
        'forecasted_drops',
        'imagens_count'
    ]
    list_filter = ['status_envio', 'data', 'user']
    search_fields = ['user__username']
    date_hierarchy = 'data'
    
    def imagens_count(self, obj):
        return obj.imagens.count()
    imagens_count.short_description = "Qtd Imagens"

# Admin simples para RelatorioImagem
admin.site.register(RelatorioImagem)
