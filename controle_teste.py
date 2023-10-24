# Este é um programa simples que mostra como receber as mensagens enviadas
# pelo programa de controle do TP2, até para confirmar que ele está
# enviando as mensagens corretamente. 
# Ele espera receber como parâmetro o porto onde deve receber as mensagens.
# Considerando que o arquivo roteadores.txt distribuído com o código seja
# usado, ele define que o roteador terra executará na máquina local, no
# porto 5555. Dessa forma, se você iniciar este programa com o parâmetro
# 5555, ele vai se comportar como o roteador denominado terra.
# 
# Note que, segundo o enunciado do TP2, o roteador vai receber seu nome e o
# nome do arquivo com os roteadores, aí ele poderá extrair da informação do
# arquivo o número do porto que ele deverá usar.
# 
# DICA: o código do programa de controle já tem o exemplo de como o arquivo
# de roteadores deve ser processado.

import socket
import sys
from socket import AF_INET, SOCK_DGRAM
from struct import *

# Essas funções "extrai" retiram as informações da mensagem recebida.
# Para mostrar como extrair partes quaisquer de um vetor de bytes,
# elas são mais complexas do que precisava, incluindo a posição do vetor
# a partir da qual elas vão extrair os dados (i)

def extrai_roteador(msg,i):
    r = unpack(">32s",msg[i:i+32]) 
    return r[0].decode()

def extrai_destino_texto(msg,i):
    l = unpack(">32s64s",msg[i:i+96]) # 96 = 32 + 64
    destino = l[0].decode()
    texto   = l[1].decode()
    return destino, texto

# Atenção: quando for necessário ir decodificando as diversas linhas
#          de um vetor de distâncias, é importante usar o recurso
#          de python de selecionar faixas de um vetor de bytes:
#          p.ex., vetor[i:i+32] indica os 32 bytes a partir da posição i.

server_socket = socket.socket(AF_INET, SOCK_DGRAM)
server_port = int(sys.argv[1])
server_socket.bind(('',server_port))
while(True):
    msg, addr_from = server_socket.recvfrom(1024)
    # print(msg, addr_from)
    c = unpack(">c",msg[0:1])
    comando = c[0].decode()
    if comando=='C' or comando=='D':
        roteador = extrai_roteador(msg,1)
        print(comando, roteador)
    elif comando=='E':
        destino, texto = extrai_destino_texto(msg,1)
        print("%s %s '%s'" % (comando, destino, texto) )
    elif comando=='T' or comando=='I':
        print(comando)
    else:
        print("Comando não reconhecido")
        
