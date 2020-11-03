"""
TRABALHO COM SOCKETS

Arquivo: client.py
Nome: Vinicius Bagolin Copetti
Data: 03/11/2020
Versao: 1.0
"""

import socket     # Biblioteca de sockets
import threading  # Biblioteca de threads


# Thread do Servidor
def thread_servidor(conexao, servidor_nome, client_nome):
    mensagem_servidor = conexao.recv(1024)          # Mensagem recebida do servidor
    mensagem_servidor = mensagem_servidor.decode()  # Decodificando para UTF-8
    print(f'\n{servidor_nome} : {mensagem_servidor}\n{client_nome} : ', end='')  # Imprimindo a mensagem


socket_servidor = socket.socket()  # Objeto Socket

# Inicialização e confirurações do servidor
print('Client Inicializado!')
servidor_ip = input('Digite o IP do Servidor: ')
porta = 6996
nome_cli = input('Digite o seu nome: ')

socket_servidor.connect((servidor_ip, porta))  # Conectar ao servidor

# Verificar se o servidor já está roadando
try:
    socket_servidor.send(nome_cli.encode())              # Envia nome do cliente para o servidor
    servidor_nome_ret = socket_servidor.recv(1024)       # Recebe o nome do cliente
    servidor_nome_ret = servidor_nome_ret.decode()       # Decodifica para UTF-8 o nome do servidor
    print(servidor_nome_ret, ' entrou na conversa...')
except ConnectionRefusedError as e:
    print('ERRO: Servidor não inicializado, tente novamente')  # Caso der erro
    print(str(e))
    exit(1)  # Finaliza a execução

fim = False
while not fim:
    # Inicialização da Thread
    thr = threading.Thread(target=thread_servidor, args=(socket_servidor, servidor_nome_ret, nome_cli))
    thr.start()  # Executa a Th = input(nome_cli + ' : ')
    # Trehad inicializada.
    mensagem = input(nome_cli + ' : ')
    if mensagem == 'FIM':
        socket_servidor.send(mensagem.encode())  # envia mensagem de FIM para o Client
        socket_servidor.close()                  # Fecha a conexão e desabilita o servidor
        fim = True                               # Finaliza loop
        print('Finalizando Client...')
        thr.join()                               # Finaliza Thread
    else:
        socket_servidor.send(mensagem.encode())  # Envia mensagem para o Servidor

print('Client Desconectado, aguardando o servidor encerrar...')

