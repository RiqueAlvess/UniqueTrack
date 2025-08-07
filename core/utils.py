import smtplib, ssl

def smtp_test(cfg):
    context = ssl.create_default_context()
    server = smtplib.SMTP(cfg.smtp_host, cfg.smtp_port, timeout=10)
    try:
        server.starttls(context=context)
        server.login(cfg.smtp_email, cfg.smtp_password)
    finally:
        server.quit()
