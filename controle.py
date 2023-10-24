# Programa a ser usado para controlar os roteadores desenvolvidos para o TP2.
# 
# Ele deve ser iniciado com apenas um argumento, que será o nome do arquivo
# contendo a identificação dos roteadores a serem usados.
# Junto com esse código você encontrará o arquivo roteadores.txt, que tem 
# a definição de quatro roteadores, sendo que os dois primeiros usam
# endereços IP ou nomes de máquinas específicas, o que seria usado se o
# TP for testado usando programas executando em mais de uma máquina.
# Os dois últimos indicam programas executando no localhost e poderiam ser
# usados como dois programas de teste, executando nas portas 55555 e 54321
# da máquina local.
# 
# Para usar o programa com o arquivo de roteadores fornecido, bastaria
# passar "roteadores.txt" como parâmetro.

import socket
from struct import *
import sys

from socket import AF_INET, SOCK_DGRAM

socket = socket.socket(AF_INET, SOCK_DGRAM)
socket.bind(('',0))

addr = {}

def roteadores_ok(roteadores):
    arguments_status = True
    for roteador in roteadores:
        if roteador not in addr:
            arguments_status = False
            print("Roteador %s não definido" % (roteador))
    return arguments_status


def adiciona_link(argv):
    roteadores = argv.split(' ')
    if len(roteadores) != 2 or not roteadores_ok(roteadores):
        print("Adiciona link deve ter 2 roteadores validos")
        return
    print("Adiciona link entre",roteadores[0],"e",roteadores[1])
    msg = pack(">c32s",'C'.encode(),roteadores[0].encode())
    socket.sendto(msg,addr[roteadores[1]])
    msg = pack(">c32s",'C'.encode(),roteadores[1].encode())
    socket.sendto(msg,addr[roteadores[0]])

def remove_link(argv):
    roteadores = argv.split(' ')
    if len(roteadores) != 2 or not roteadores_ok(roteadores):
        print("Remove link deve ter 2 roteadores validos")
        return
    print("Remove link entre",roteadores[0],"e",roteadores[1])
    msg = pack(">c32s",'D'.encode(),roteadores[0].encode())
    socket.sendto(msg,addr[roteadores[1]])
    msg = pack(">c32s",'D'.encode(),roteadores[1].encode())
    socket.sendto(msg,addr[roteadores[0]])

def mostra_tabela(argv):
    roteador=argv.split(' ')
    if len(roteador)!=1 or not roteadores_ok(roteador):
        print("Mostra tabela deve ter 1 roteador")
        return
    msg = pack(">c",'T'.encode())
    socket.sendto(msg,addr[roteador[0]])

def inicia_rcrip(argv):
    if argv!='':
        print("Inicia RCRIP não espera argumentos")
        return
    msg = pack(">c",'I'.encode())
    for roteador in addr:
        socket.sendto(msg,addr[roteador])

def envia_texto(argv):
    origem, destino, texto = argv.split(' ',2)
    print("Envia '%s' para %s a partir de %s" % (texto, destino, origem) )
    if not roteadores_ok((origem,destino)):
        return
    if texto == '':
        print("Texto não fornecido")
        return
    msg = pack(">c32s64s",'E'.encode(),destino.encode(),texto.encode())
    socket.sendto(msg,addr[origem])

comandos = {'A': adiciona_link,
           'R': remove_link,
           'T': mostra_tabela,
           'I': inicia_rcrip,
           'E': envia_texto,
}

if len(sys.argv) != 2:
    print("Uso:",sys.argv[0],"nome_arquivo")
    exit(1)

f = open(sys.argv[1],'r')
roteadores = f.readlines()
for roteador in roteadores:
    rname,rhost,rport  = roteador.split(' ')
    addr[rname] = (rhost,int(rport))
    print("(",rname,"->",addr[rname],")")

while(True):
    try:
        line = input()
    except EOFError:
        break
    if line == '':
        continue
    
    ls = line.split(' ',1)
    comando = ls[0]
    if len(ls) == 1:
        argumentos = ''
    else:
        argumentos = ls[1]
    comando = comando.rstrip().upper()
    if comando not in comandos:
        print("Comando desconhecido:",comando)
        continue
    comandos[comando](argumentos)

