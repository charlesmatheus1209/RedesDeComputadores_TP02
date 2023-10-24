import socket
import sys

from socket import AF_INET, SOCK_DGRAM

if(len(sys.argv) != 3):
    print("quantidade erada de parametros")
    sys.exit()

identificador = sys.argv[1]
arquivoConfig = sys.argv[2]

print(identificador)
print(arquivoConfig)

# socket = socket.socket(AF_INET, SOCK_DGRAM)
# socket.bind(('',0))

