import socket
import sys

from socket import AF_INET, SOCK_DGRAM

if(len(sys.argv) != 3):
    print("quantidade erada de parametros")
    sys.exit()

identificador = sys.argv[1]
arquivoConfig = sys.argv[2]

print("identificador: ", identificador)
print("Arquivo: ", arquivoConfig)

socket = socket.socket(AF_INET, SOCK_DGRAM)
socket.bind((identificador,1234))

while True:
    msgFromServer = socket.recvfrom(1024)
    mensagem = msgFromServer[0].decode('utf-8')
    comando = mensagem[0]
    
    if(comando == 'C'):
        print('Comando C')
    elif(comando == 'D'):
        print('Comando D')
    elif(comando == 'T'):
        print('Comando T')
    elif(comando == 'I'):
        print('Comando I')
    elif(comando == 'E'):
        print('Comando E')
        
    