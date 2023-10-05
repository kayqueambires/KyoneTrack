import requests
import json
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import sqlite3
import os
from datetime import datetime
from time import sleep

# Substitua pelo seu SID no site do Twilio
account_sid = 'seu-account-sid'
# Substitua pelo seu auth_token no site do Twilio
auth_token = 'seu-auth-token'
# Criação do cliente para a API Twilio
client = Client(account_sid, auth_token)
# Substitua pelo seu código de rastreamento
codigo_rastreamento = 'seu-codigo-rastreamento'

# Diretório atual do script
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
# Caminho para o banco de dados SQLite
db_path = os.path.join(diretorio_atual, 'logs.db')


def conectar_bd():
    """Conecta ao banco de dados SQLite."""
    conn = sqlite3.connect(db_path)
    criar_tabela_logs(conn)
    return conn


def consultar_ultimo_log():
    """Consulta o último log no banco de dados."""
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT data_hora, mensagem FROM logs ORDER BY id DESC LIMIT 1")
    ultimo_log = cursor.fetchone()
    conn.close()
    return ultimo_log


def mensagem_ja_registrada(mensagem):
    """Verifica se uma mensagem já foi registrada no banco de dados."""
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM logs WHERE mensagem = ?", (mensagem,))
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0


def criar_tabela_logs(conn):
    """Cria a tabela de logs no banco de dados, se não existir."""
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS logs
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       data_hora DATETIME,
                       mensagem TEXT)''')
    conn.commit()


def registrar_log(mensagem):
    """Registra um novo log no banco de dados."""
    if not mensagem_ja_registrada(mensagem):
        conn = conectar_bd()
        data_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn.execute(
            "INSERT INTO logs (data_hora, mensagem) VALUES (?, ?)", (data_hora, mensagem))
        conn.commit()
        conn.close()


def obter_rastreio(codigo):
    """Obtém informações de rastreamento de um código."""
    # URL de rastreamento - Substitua pela URL desejada
    url = f"https://api.linketrack.com/track/json?user=teste&token=1abcd00b2731640e886fb41a8a9671ad1434c599dbaa0a0de9a5aa619f29a83f&codigo={codigo}"
    response = requests.get(url)

    if response.status_code == 200:
        data = json.loads(response.text)

        eventos = data.get("eventos", [])

        # Verificando se há eventos
        if eventos:
            # Pegando o último evento (índice 0)
            ultimo_evento = eventos[0]

            # Acessando os campos desse evento
            data_evento = ultimo_evento.get("data")
            hora_evento = ultimo_evento.get("hora")
            local_evento = ultimo_evento.get("local")
            status_evento = ultimo_evento.get("status")

            # Retorne os detalhes do evento (opcional)
            return f"{data_evento} - {hora_evento}\n{local_evento}\n{status_evento}"
        else:
            return "Nenhum evento encontrado."
    else:
        return "Erro ao obter dados de rastreamento."


def enviar_mensagem(mensagem):
    """Envia uma mensagem via Twilio."""
    try:
        message = client.messages.create(
            from_='whatsapp:+0123456789',  # Substitua pelo número do Twilio
            body=f'Nova atualização na entrega do seu pedido.\n{mensagem}',
            to='whatsapp:+0123456789'  # Substitua pelo seu número do Whatsapp
        )
        # Caso nenhum erro ocorra, exibe uma confirmação
        print("Mensagem enviada com sucesso!")
    except TwilioRestException as e:
        # Exceção específica para erros da API Twilio
        print(f"Erro Twilio: {e}")
    except Exception as e:
        # Captura qualquer outra exceção
        print(f"Erro desconhecido: {e}")


def executar_main(codigo_rastreamento):
    """Função principal para rastreamento."""
    print("Executando rastreamento...")
    rastreamento = obter_rastreio(codigo_rastreamento)

    ultimo_log = consultar_ultimo_log()

    # Verificar se a mensagem é igual à última mensagem registrada
    if not ultimo_log or rastreamento != ultimo_log[1]:
        if not mensagem_ja_registrada(rastreamento):
            registrar_log(rastreamento)
            enviar_mensagem(rastreamento)
    else:
        print('Atualização já registrada.')


if __name__ == '__main__':
    codigo_rastreamento = codigo_rastreamento
    while True:
        executar_main(codigo_rastreamento)
        sleep(7200)  # Intervalo de 2 horas entre as execuções
