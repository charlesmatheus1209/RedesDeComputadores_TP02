from struct import *

str1 = "Arroz0"
b = bytes()
b += b"A"
b += b"r"
b += b"r"
b += b"o"
b += b"z"
b += b"0"
print(b)
packed = pack("c32s", "D".encode(), b)

unpacked = unpack("c32s", packed)

# print(unpacked[1].rstrip(b'\x00').decode() == "Arro0z0")
# print(unpacked[1].rstrip(b'\x00').decode())

print(unpacked[1].decode())
print(str1)

print(len(unpacked[1].rstrip(b'\x00').decode()))
print(len(str1))

print(unpacked[1].rstrip(b'\x00').decode() == str1)