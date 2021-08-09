import smtplib, ssl, os

port = 465
smtp_server = "smtp.gmail.com"
user = os.getenv('GMAIL_USER')
password = os.getenv('GMAIL_PASSWORD')
receiver_email = os.getenv('RECEIVER_EMAIL')

message = """\
Subject: Procesos judiciales - Rolando

Lista de procesos activos:

{active_processes}

Lista de procesos que NO fueron procesados por fallos internos o porque no estan soportados:

{failed_processes}

Que tengas un feliz dia!"""

context = ssl.create_default_context()

def send_email(active_processes, failed_processes):
    print("Gmail: sending gmail update")
    active_processes_message = ''
    for process in active_processes:
        active_processes += process + '\n'
    failed_processes_message = ''
    for process in failed_processes:
        failed_processes += process + '\n'
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(user, password)
        server.sendmail(
            user,
            receiver_email,
            message.format(active_processes=active_processes_message, failed_processes=failed_processes_message))
        print('Gmail: email sent')
