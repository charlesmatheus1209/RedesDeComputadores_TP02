import socket
import sys
import time

from socket import AF_INET, SOCK_DGRAM



tabelaRoteamento = dict()
tabelaEnderecos = dict()
timer = time.t

    

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
    print("Função: enviaMensagem()", dest, " -- ", mensagem)
    print(tabelaEnderecos[dest])
    
    udp = socket.socket(AF_INET, SOCK_DGRAM)
    udp.sendto(bytes(mensagem, 'utf-8'), tabelaEnderecos[dest])
    print(tabelaRoteamento[dest][0])
    if(tabelaRoteamento[dest][0] == dest):
        print("R", mensagem)
    else:
        print("E", dest, mensagem)
    
    
    
    
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
socket_.bind((identificador,1234))


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
    elif(comando == 'E'):
        print('Comando E')
        destino = msgFromServer[0][1:msgFromServer[0].find(b'\x00')].decode('utf-8')
        enviaMensagem(destino, mensagem[len(destino)+1:])
    
    mostraTabela()
        
    