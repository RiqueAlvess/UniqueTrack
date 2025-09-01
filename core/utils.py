import requests
import json

def smtp_test(cfg):
    """Testa a conexão com a API de e-mail"""
    api_url = 'https://b17e248dbc8e.ngrok-free.app/send-email'
    
    # Pega EXATAMENTE do banco e entrega para API
    payload = {
        "email": str(cfg.smtp_email),           # garantir que é string
        "password": str(cfg.smtp_password),     # garantir que é string
        "to": [str(cfg.smtp_email)],           # teste: envia para si mesmo
        "subject": "Teste de Configuração - Sistema de Relatórios",
        "body": "Este é um e-mail de teste para verificar se a API está funcionando corretamente.",
        "debug": True,
        "headless": False
    }
    
    print(f"DEBUG - Enviando para API:")
    print(f"  Email: {payload['email']}")
    print(f"  Password length: {len(payload['password'])}")
    print(f"  To: {payload['to']}")
    
    headers = {'Content-Type': 'application/json'}
    
    response = requests.post(
        api_url,
        headers=headers,
        json=payload,  # usando .json ao invés de data=json.dumps
        timeout=30
    )
    
    print(f"  Response status: {response.status_code}")
    print(f"  Response: {response.text[:200]}...")  # primeiros 200 chars
    
    if response.status_code != 200:
        raise Exception(f"API retornou status {response.status_code}: {response.text}")
    
    return response.json()

def send_email_via_api(cfg, to_emails, subject, body):
    """Envia e-mail através da API"""
    api_url = 'https://b17e248dbc8e.ngrok-free.app/send-email'
    
    # Pega EXATAMENTE do banco e entrega para API
    payload = {
        "email": str(cfg.smtp_email),
        "password": str(cfg.smtp_password),
        "to": [str(email) for email in to_emails],  # garantir que todos são strings
        "subject": str(subject),
        "body": str(body),
        "debug": True,
        "headless": False
    }
    
    print(f"DEBUG - Enviando relatório:")
    print(f"  Email: {payload['email']}")
    print(f"  Password length: {len(payload['password'])}")
    print(f"  To: {payload['to']}")
    print(f"  Subject: {payload['subject'][:50]}...")
    
    headers = {'Content-Type': 'application/json'}
    
    response = requests.post(
        api_url,
        headers=headers,
        json=payload,  # usando .json ao invés de data=json.dumps
        timeout=60
    )
    
    print(f"  Response status: {response.status_code}")
    print(f"  Response: {response.text[:200]}...")
    
    if response.status_code != 200:
        raise Exception(f"Falha no envio. Status {response.status_code}: {response.text}")
    
    return response.json()
