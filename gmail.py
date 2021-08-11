import smtplib, ssl, os, logging

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
    logging.info("Gmail: sending gmail update")
    active_processes_message = ''
    for process in active_processes:
        active_processes_message += process + '\n'
    failed_processes_message = ''
    for process in failed_processes:
        failed_processes_message += process + '\n'
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(user, password)
        server.sendmail(
            user,
            receiver_email,
            message.format(
                active_processes=active_processes_message if active_processes_message else 'No hay procesos activos!',
                failed_processes=failed_processes_message if failed_processes_message else 'Todos los procesos se validaron exitosamente!'))
        logging.info('Gmail: email sent')
