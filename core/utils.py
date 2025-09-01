import requests
import json

def smtp_test(cfg):
    """Testa a conexão com a API de e-mail"""
    api_url = 'https://b17e248dbc8e.ngrok-free.app/send-email'
    
    payload = {
        "email": cfg.smtp_email,
        "password": cfg.smtp_password,
        "to": [cfg.smtp_email],  # envia para si mesmo como teste
        "subject": "Teste de Configuração - Sistema de Relatórios",
        "body": "Este é um e-mail de teste para verificar se a API está funcionando corretamente.",
        "debug": True,
        "headless": False
    }
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.post(
        api_url,
        headers=headers,
        data=json.dumps(payload),
        timeout=30
    )
    
    if response.status_code != 200:
        raise Exception(f"API retornou status {response.status_code}: {response.text}")
    
    return response.json()

def send_email_via_api(cfg, to_emails, subject, body):
    """Envia e-mail através da API"""
    api_url = 'https://b17e248dbc8e.ngrok-free.app/send-email'
    
    payload = {
        "email": cfg.smtp_email,
        "password": cfg.smtp_password,
        "to": to_emails,
        "subject": subject,
        "body": body,
        "debug": True,
        "headless": False
    }
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.post(
        api_url,
        headers=headers,
        data=json.dumps(payload),
        timeout=60
    )
    
    if response.status_code != 200:
        raise Exception(f"Falha no envio. Status {response.status_code}: {response.text}")
    
    return response.json()
