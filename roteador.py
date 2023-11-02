# Nome1: Marielle Cristina Silva Costa - Matricula: 2021014805
# Nome2: Charles Matheus de Souza Soares Nascimento - Matricula: 2021014821

import socket
from struct import *
import sys

import threading

from socket import AF_INET, SOCK_DGRAM

# Intervalo para compartilhamento de tabelas!
timeout_seconds = 1

#Custo Máximo aceitável para conectar dois nós
CustoMaximo = 16

tabelaRoteamento = dict()
tabelaEnderecos = dict()

bloqueioComandoI = True


def CompartilhaTabelaRoteamento():
    #Formato da mensagem:
    #J-ORIGEM-Tabela  <- USANDO O PACK E UNPACK
    # print("Iniciando compartilhamento da Tabela de Roteamento")
    
    try:
        chaves = tabelaRoteamento.keys()
        Tabela = []
        for chave in chaves:
            if(chave != identificador):
                Tabela.append(identificador + "--" + chave + "--" + tabelaRoteamento[chave][0] + "--" + str(tabelaRoteamento[chave][1]))
        
        b = bytearray()
        b += bytes("J", 'utf-8')
        for string in Tabela:
            bs = string.encode()
            b += pack("=I", len(bs)) + bs
            
        # print("Mostrando mensagem")
        # print(b)
        
        udp = socket.socket(AF_INET, SOCK_DGRAM)
        chaves = tabelaRoteamento.keys()
        for chave in chaves:
            if(chave in tabelaRoteamento.keys()):
                if(chave != identificador and tabelaRoteamento[chave][1] == 1):
                    udp.sendto(b,tabelaEnderecos[chave])
        
        udp.close()
        # while b:
        #     length, *_ = unpack("=I", b[:4])
        #     print(b[4:length+4].decode())
        #     b = b[length+4:]
        timer = threading.Timer(timeout_seconds, CompartilhaTabelaRoteamento)
        timer.start()
    except:
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
    # print("Função: criaConexao()", comando)
    comando = comando.replace("\x00", '')
    tabelaRoteamento[comando] = (comando, 1)
    
def deletaConexao(comando):
    # print("Função: deletaConexao()", comando)
    comando = comando.replace('\x00', '')
    if(comando in tabelaRoteamento):
        del tabelaRoteamento[comando]
    
    chaves = tabelaRoteamento.keys()
    proximosPassos = []
    for chave in chaves:
        if(tabelaRoteamento[chave][0] == comando):
            proximosPassos.append(chave)
        
    for chave in proximosPassos:
        del tabelaRoteamento[chave]
            
        
def enviaMensagem(dest, mensagem): 
    # Formato da mensagem:
    # pack(S,ORIGEM,DESTINO,MENSAGEM)  <- USANDO O PACK E UNPACK
    # print("Função: enviaMensagem(), Destino: '", dest, "' -- Mensagem: '", mensagem,"'")
    
    if(dest in tabelaRoteamento.keys()):
        udp = socket.socket(AF_INET, SOCK_DGRAM)
        proximo = tabelaRoteamento[dest][0]
        mensagemEnviar = pack(">c32s32s64s", 'S'.encode(), identificador.encode(), dest.encode(), mensagem.encode())
        udp.sendto(mensagemEnviar, tabelaEnderecos[proximo])
        udp.close()
    else:
        print("O destino '", dest ,"' não está na tabela de roteamento de '", identificador, "'")   
    
def mostraTabela():
    # print("Função: mostraTabela()")
    chaves = tabelaRoteamento.keys()
    for chave in chaves:
        print(chave, tabelaRoteamento[chave][0], tabelaRoteamento[chave][1])

def processaTabelaRecebida(tabelaRecebida, origem):
    # print("Função: processaTabelaRecebida(), Tabela: '", tabelaRecebida, "' de: ", origem)
    
    for destino in tabelaRecebida.keys():
        # print(destino)
        if(destino in tabelaRoteamento.keys()):
            # print("Já existe na minha tabela")
            if(tabelaRoteamento[destino][0] == origem and tabelaRecebida[destino][1] > tabelaRoteamento[destino][1]):
                if(tabelaRoteamento[destino][1] > CustoMaximo):
                    deletaConexao(destino)
                else:
                    tabelaRoteamento[destino] = tabelaRecebida[destino]
            elif(tabelaRecebida[destino][1] < tabelaRoteamento[destino][1]):
                if(tabelaRoteamento[destino][1] > CustoMaximo):
                    deletaConexao(destino)
                else:
                    tabelaRoteamento[destino] = tabelaRecebida[destino]
        else:
            # print("É novo para mim")
            if(tabelaRecebida[destino][1] <= CustoMaximo):
                tabelaRoteamento[destino] = tabelaRecebida[destino]
                
    
def analisaTabelaRoteamento():
    # print("Função: analisaTabelaRoteamento()")
    chaves = tabelaRoteamento.keys()
    chavesParaDeletar = []
    for chave in chaves:
        if(tabelaRoteamento[chave][1] > CustoMaximo):
            chavesParaDeletar.append(chave)
    
    
    for chave in chavesParaDeletar:
        deletaConexao(chave)
 
if(len(sys.argv) != 3):
    # print("quantidade erada de parametros")
    sys.exit()

identificador = sys.argv[1]
arquivoConfig = sys.argv[2]

print("identificador: ", identificador)
print("Arquivo: ", arquivoConfig)


tabelaRoteamento[identificador] = (identificador, 0)
leituraDoArquivo(arquivoConfig)

socket_ = socket.socket(AF_INET, SOCK_DGRAM)
socket_.bind(tabelaEnderecos[identificador])



while True:
    msgFromServer = socket_.recvfrom(1024)
    analisaTabelaRoteamento()
    mensagem = msgFromServer[0].decode('utf-8')
    comando = mensagem[0] 
    
    if(comando == 'C'):
        # print('Comando C')
        criaConexao(mensagem[1:])
    elif(comando == 'D'):
        # print('Comando D')
        deletaConexao(mensagem[1:])
    elif(comando == 'T'):
        # print('Comando T')
        mostraTabela()
    elif(comando == 'I'):
        # print('Comando I')
        
        if(bloqueioComandoI):
            # Iniciando o temporizador
            timer = threading.Timer(timeout_seconds, CompartilhaTabelaRoteamento)
            timer.start()
            bloqueioComandoI = False

    elif(comando == 'E'):
        # print('Comando E')        
        unpacked = unpack(">c32s64s", msgFromServer[0])
        enviaMensagem(unpacked[1].rstrip(b'\x00').decode('utf-8'), unpacked[2].decode('utf-8'))
    elif(comando == 'S'): #Mensagem recebida de outro roteador
        # print('Comando S')  
        unpacked = unpack(">c32s32s64s", msgFromServer[0])
        if(unpacked[2].rstrip(b'\x00').decode('utf-8') == identificador):
            print("R", unpacked[3].rstrip(b'\x00').decode('utf-8'))
        else:
            destino = unpacked[2].rstrip(b'\x00').decode('utf-8')
            mensagemParaEnviar = unpacked[3].rstrip(b'\x00').decode('utf-8')
            if(destino in tabelaRoteamento.keys()):
                proximoPasso = tabelaRoteamento[destino][0]
                print("E", destino, mensagemParaEnviar, proximoPasso)
                enviaMensagem(destino, mensagemParaEnviar)
            else:
                print(f"{destino} não está na tabela de roteamento de {identificador}")
            
    elif(comando == "J"):
        # print('Comando J')  
        tabelaRecebida = dict() #destino = (caminho, custo)
        
        b = msgFromServer[0][1:]
        while b:
            length, *_ = unpack("=I", b[:4])
            # print(b[4:length+4].decode().split("--"))
            received = b[4:length+4].decode().split("--")
            tabelaRecebida[received[1]] = (received[0], int(received[3]) + 1)
            b = b[length+4:]
        
        # print("Tabela Recebida: ")
        # print(tabelaRecebida)
        origem = received[0]
        processaTabelaRecebida(tabelaRecebida, origem)
        
    else:
        print("estou no else")
        
    
    # mostraTabela()
        
    