import socket
from struct import *
import sys

import threading

from socket import AF_INET, SOCK_DGRAM



tabelaRoteamento = dict()
tabelaEnderecos = dict()

timeout_seconds = 2


def CompartilhaTabelaRoteamento():
    #Formato da mensagem:
    #J-ORIGEM-Tabela  <- USANDO O PACK E UNPACK
    print("Iniciando compartilhamento da Tabela de Roteamento")
    
    chaves = tabelaRoteamento.keys()
    Tabela = []
    for chave in chaves:
        Tabela.append(identificador + "--" + chave + "--" + tabelaRoteamento[chave][0] + "--" + str(tabelaRoteamento[chave][1]))
    
    b = bytearray()
    b += bytes("J", 'utf-8')
    for string in Tabela:
        bs = string.encode()
        b += pack("=I", len(bs)) + bs
        
    # print("Mostrando mensagem")
    # print(b)
    
    udp = socket.socket(AF_INET, SOCK_DGRAM)
    for chave in tabelaRoteamento.keys():
        udp.sendto(b,tabelaEnderecos[chave])
    
    udp.close()
    # while b:
    #     length, *_ = unpack("=I", b[:4])
    #     print(b[4:length+4].decode())
    #     b = b[length+4:]
    
    
    
    timer = threading.Timer(timeout_seconds, CompartilhaTabelaRoteamento)
    timer.start()


    

def leituraDoArquivo(nomeArquivo):
    arquivo= open(nomeArquivo,'r')
    
    linhas = arquivo.readlines()
    for linha in linhas:
        linha = linha.replace('\n', '')
        id, endereco, porta = linha.split(' ')
        p = int(porta)
        tabelaEnderecos[id] = (endereco, p)    

def criaConexao(comando):
    print("Função: criaConexao()", comando)
    comando = comando.replace("\x00", '')
    tabelaRoteamento[comando] = (comando, 1)
    
def deletaConexao(comando):
    print("Função: deletaConexao()", comando)
    comando = comando.replace('\x00', '')
    if(comando in tabelaRoteamento):
        del tabelaRoteamento[comando]
        
def enviaMensagem(dest, mensagem): 
    #Formato da mensagem:
    #S-ORIGEM-DESTINO-MENSAGEM  <- USANDO O PACK E UNPACK
    print("Função: enviaMensagem(), Destino: '", dest, "' -- Mensagem: '", mensagem,"'")
    
    chaves = tabelaRoteamento.keys()
    if(dest in chaves):
        udp = socket.socket(AF_INET, SOCK_DGRAM)
        mensagemEnviar = pack(">c32s32s64s", 'S'.encode(), identificador.encode(), dest.encode(), mensagem.encode())
        udp.sendto(mensagemEnviar, tabelaEnderecos[dest])
        udp.close()
    else:
        print("O destino '", dest ,"' não está na tabela de roteamento de '", identificador, "'")
    
    
def mostraTabela():
    print("Função: mostraTabela()")
    chaves = tabelaRoteamento.keys()
    for chave in chaves:
        print(chave, tabelaRoteamento[chave][0], tabelaRoteamento[chave][1])
        
    
if(len(sys.argv) != 3):
    print("quantidade erada de parametros")
    sys.exit()

identificador = sys.argv[1]
arquivoConfig = sys.argv[2]

print("identificador: ", identificador)
print("Arquivo: ", arquivoConfig)


leituraDoArquivo(arquivoConfig)

socket_ = socket.socket(AF_INET, SOCK_DGRAM)
socket_.bind(tabelaEnderecos[identificador])



while True:
    msgFromServer = socket_.recvfrom(1024)
    mensagem = msgFromServer[0].decode('utf-8')
    comando = mensagem[0] 
    
    if(comando == 'C'):
        print('Comando C')
        criaConexao(mensagem[1:])
    elif(comando == 'D'):
        print('Comando D')
        deletaConexao(mensagem[1:])
    elif(comando == 'T'):
        print('Comando T')
        mostraTabela()
    elif(comando == 'I'):
        print('Comando I')
        # Iniciando o temporizador
        timer = threading.Timer(timeout_seconds, CompartilhaTabelaRoteamento)
        timer.start()

    elif(comando == 'E'):
        print('Comando E')        
        unpacked = unpack(">c32s64s", msgFromServer[0])
        enviaMensagem(unpacked[1].split(b'\x00')[0].decode('utf-8'), unpacked[2].decode('utf-8'))
    elif(comando == 'S'): #Mensagem recebida de outro roteador
        print('Comando S')  
        unpacked = unpack(">c32s32s64s", msgFromServer[0])
        if(unpacked[2].split(b'\x00')[0].decode('utf-8') == identificador):
            print("R")
        else:
            destino = unpacked[2].split(b'\x00')[0].decode('utf-8')
            mensagemParaEnviar = unpacked[3].split(b'\x00')[0].decode('utf-8')
            proximoPasso = tabelaRoteamento[destino][0]
            print("E", destino, mensagemParaEnviar, proximoPasso)
    elif(comando == "J"):
        print('Comando J')  
        
        b = msgFromServer[0][1:]
        print(b)
        while b:
            length, *_ = unpack("=I", b[:4])
            print(b[4:length+4].decode())
            b = b[length+4:]
    else:
        print("estou no else")
        
    
    mostraTabela()
        
    