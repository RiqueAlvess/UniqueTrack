import requests
import json

def smtp_test(cfg):
    """Testa a conexão com a API de e-mail"""
    api_url = 'https://b17e248dbc8e.ngrok-free.app/send-email'
    
    payload = {
        "email": str(cfg.smtp_email),
        "password": str(cfg.smtp_password),
        "to": [str(cfg.smtp_email)],
        "subject": "Teste de Configuração - Sistema de Relatórios",
        "body": "Este é um e-mail de teste para verificar se a API está funcionando corretamente.",
        "debug": True,
        "headless": False
    }
    
    print(f"DEBUG - Teste API:")
    print(f"  Email: {payload['email']}")
    print(f"  Password length: {len(payload['password'])}")
    
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(
            api_url,
            headers=headers,
            json=payload,
            timeout=600  # 10 minutos - API MVP pode ser lenta
        )
        
        print(f"  Response status: {response.status_code}")
        print(f"  Response: {response.text[:300]}...")
        
        # Verificar se HTTP status é 200
        if response.status_code != 200:
            raise Exception(f"API retornou HTTP {response.status_code}: {response.text}")
        
        # Tentar fazer parse do JSON
        try:
            response_data = response.json()
        except json.JSONDecodeError as e:
            raise Exception(f"Erro ao fazer parse da resposta JSON: {e}")
        
        # Verificar se a API indica sucesso
        # A API retorna: {"status": "sucesso", "data": {"success": true, ...}}
        api_status = response_data.get('status', '')
        api_success = response_data.get('data', {}).get('success', False)
        
        if api_status != 'sucesso' and not api_success:
            error_msg = response_data.get('message', 'Erro desconhecido')
            raise Exception(f"API retornou erro: {error_msg}")
        
        print(f"  ✅ API retornou sucesso!")
        return response_data
        
    except requests.exceptions.Timeout:
        raise Exception("Timeout: API demorou mais de 10 minutos para responder (MVP pode ser lenta)")
    except requests.exceptions.ConnectionError:
        raise Exception("Erro de conexão: Não foi possível conectar com a API")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Erro na requisição: {e}")

def send_email_via_api(cfg, to_emails, subject, body):
    """Envia e-mail através da API"""
    api_url = 'https://b17e248dbc8e.ngrok-free.app/send-email'
    
    payload = {
        "email": str(cfg.smtp_email),
        "password": str(cfg.smtp_password),
        "to": [str(email) for email in to_emails],
        "subject": str(subject),
        "body": str(body),
        "debug": True,
        "headless": False
    }
    
    print(f"DEBUG - Envio via API:")
    print(f"  Email: {payload['email']}")
    print(f"  Password length: {len(payload['password'])}")
    print(f"  Para: {payload['to']}")
    print(f"  Assunto: {payload['subject'][:50]}...")
    
    headers = {'Content-Type': 'application/json'}
    
    try:
        print("  🚀 Enviando para API... (pode demorar até 10 minutos)")
        
        response = requests.post(
            api_url,
            headers=headers,
            json=payload,
            timeout=600  # 10 minutos - API MVP pode ser bem lenta
        )
        
        print(f"  ✅ Response recebida!")
        print(f"  Status HTTP: {response.status_code}")
        print(f"  Response preview: {response.text[:300]}...")
        
        # Verificar se HTTP status é 200
        if response.status_code != 200:
            raise Exception(f"API retornou HTTP {response.status_code}: {response.text}")
        
        # Tentar fazer parse do JSON
        try:
            response_data = response.json()
            print(f"  📦 JSON parseado com sucesso!")
        except json.JSONDecodeError as e:
            print(f"  ❌ Erro no parse JSON: {e}")
            raise Exception(f"Erro ao fazer parse da resposta JSON: {e}")
        
        # Verificar se a API indica sucesso
        api_status = response_data.get('status', '')
        api_success = response_data.get('data', {}).get('success', False)
        
        print(f"  Status da API: {api_status}")
        print(f"  Success flag: {api_success}")
        
        if api_status != 'sucesso' and not api_success:
            error_msg = response_data.get('message', 'Erro desconhecido')
            raise Exception(f"API retornou erro: {error_msg}")
        
        print(f"  🎉 E-mail enviado com sucesso via API!")
        
        # Pegar dados adicionais se disponível
        sent_at = response_data.get('data', {}).get('sentAt', '')
        processing_time = response_data.get('data', {}).get('totalProcessingTime', 0)
        
        if sent_at:
            print(f"  📅 Enviado em: {sent_at}")
        if processing_time:
            print(f"  ⏱️ Tempo total: {processing_time/1000:.1f}s")
        
        return response_data
        
    except requests.exceptions.Timeout:
        raise Exception("Timeout: API demorou mais de 90 segundos (normal: até 60s)")
    except requests.exceptions.ConnectionError:
        raise Exception("Erro de conexão: Não foi possível conectar com a API")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Erro na requisição: {e}")
