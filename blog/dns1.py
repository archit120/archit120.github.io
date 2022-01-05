import socket
import base64

server = "198.41.0.4"
port = 53

message_hex = "010000000001000000000000076369746164656C03636F6D0000010001"
message_binary = base64.b16decode(message_hex, True)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(message_binary, (server, port))
data, _ = sock.recvfrom(1024)

data = data + b'\0'*(4-len(data)%4)

ascii_str = data.decode("ascii", "replace")
hex_str = base64.b16encode(data).decode("ascii")

for i in range(0, len(hex_str), 4):
    print("{0} {1} | {2} {3}".format(hex_str[i:i+2], hex_str[i+2:i+4], ascii_str[i//2], ascii_str[i//2+1]))
