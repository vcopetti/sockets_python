"""
TRABALHO COM SOCKETS

Arquivo: server.py
Nome: Vinicius Bagolin Copetti
Data: 03/11/2020
Versao: 1.0
"""

import socket  # Biblioteca de Sockets
import threading  # Biblioteca de threads


# Thread do cliente
def thread_client(conexao, cliente_nome, servidor_nome):
    mensagem_cliente = conexao.recv(1024)         # Mensagem recebida do cliente
    mensagem_cliente = mensagem_cliente.decode()  # Decodificando para UTF-8
    print(f'\n{cliente_nome} : {mensagem_cliente}\n{servidor_nome} : ', end='')  # Imprimindo a mensagem


print('Iniciando Serivor...')
srv_socket = socket.socket()  # inicializando o socket do servidor
meu_ip = '127.0.0.1'          # IP do servidor
porta = 6996                  # Porta padrão

# Verificar se o servidor já está roadando
try:
    srv_socket.bind((meu_ip, porta))                      # Ligando o servidor no IP e na porta definidos acima
except socket.error as e:
    print('ERRO: Servidor em execução, tente novamente')  # Caso der erro
    print(str(e))
    exit(1)  # Finaliza a execução

# Informando os parametros de inicialização do servidor
print('Servidor Inicializado !')
print('IP: ',  meu_ip)
print('Porta: ', porta)

nome_servidor = input('Digite o seu nome: ')  # Nome do usuário que está no servidor

srv_socket.listen(1)                        # Habilita conexões e aguarda. Parametro identifica numero máximo de clients
print(f'OK, {nome_servidor}. Aguardando Conexão...')
conn, ip_client = srv_socket.accept()         # Aceita a conexão e retorna o IP do client e um objeto socket

client_nome_ret = (conn.recv(1024)).decode()  # Client enviou o seu nome
print(f'{client_nome_ret} se conectou a partir do IP: {ip_client[0]}')
conn.send(nome_servidor.encode())             # Envia o meu nome para o client
fim = False

while not fim:
    thr = threading.Thread(target=thread_client, args=(conn, client_nome_ret, nome_servidor))  # parametros iniciais da Thread
    thr.start()  # Executa a Thread
    mensagem = input(nome_servidor + ' : ')
    if mensagem == 'FIM':
        conn.send(mensagem.encode())  # envia mensagem de FIM para o Client
        conn.close()                  # Fecha a conexão e desabilita o servidor
        fim = True
        print('Finalizando Servidor...')
        thr.join()                    # Finaliza a Thread
    else:
        conn.send(mensagem.encode())  # envia a mensagem ao client


print('Servidor Finalizado')
