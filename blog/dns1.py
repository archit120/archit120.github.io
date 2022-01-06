from abc import ABC
from ctypes import resize
import socket
import base64
import struct
from typing import Tuple

server = "198.41.0.4"
port = 53

message_hex = "010000000001000000000000076369746164656C03636F6D0000010001"
message_binary = base64.b16decode(message_hex, True)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(message_binary, (server, port))
data_orig, _ = sock.recvfrom(1024)

data = data_orig + b'\0'*(4-len(data_orig)%4)

ascii_str = data.decode("ascii", "replace")
hex_str = base64.b16encode(data).decode("ascii")

for i in range(0, len(hex_str), 4):
    print("{0} {1} | {2} {3}".format(hex_str[i:i+2], hex_str[i+2:i+4], ascii_str[i//2], ascii_str[i//2+1]))


class PrettyPrinter(object):
    def __str__(self):
        lines = [self.__class__.__name__ + ':']
        for key, val in vars(self).items():
            lines += '{}: {}'.format(key, val).split('\n')
        return '\n    '.join(lines)
    def __repr__(self) -> str:
        return self.__str__()

class Header(PrettyPrinter):
    def __init__(self, data: bytes) -> None:
        self.ID, flags, self.QDCount, self.ANCount, self.NSCount, \
            self.ARCount = struct.unpack(">HHHHHH", data[:12])
        
        self.QR = ((flags & (1<<15))!=0)
        self.Opcode = (flags >> 11)&0b1111
        self.AA = ((flags & (1<<10))!=0)
        self.TC = ((flags & (1<<9))!=0)
        self.RD = ((flags & (1<<8))!=0)
        self.RA = ((flags & (1<<7))!=0)
        self.Z = (flags >> 4) &0b111
        self.RCODE = flags & 0b1111

def read_string(data: bytes, start_pos: int) -> Tuple[str, int]:
    retstr = ''
    while True:
        length = data[start_pos]
        start_pos+=1
        if length == 0:
            return retstr[1:], start_pos
        elif length>63:
            length, = struct.unpack(">H", data[start_pos-1:start_pos+1])
            length -= 0xC000
            return (retstr+'.'+read_string(data, length)[0])[1:], start_pos+1
        retstr = retstr + '.' + data[start_pos:start_pos+length].decode('ascii')
        start_pos += length


class Question(PrettyPrinter):

    def __init__(self, data: bytes, start_pos: int) -> None:
        self.QName, start_pos = read_string(data, start_pos)
        self.QType, self.QClass = struct.unpack(">HH", data[start_pos:start_pos+4])
        self.end_pos = start_pos+4        

class ARData(PrettyPrinter):
    def __init__(self, data: bytes, start_pos: int) -> None:
        self.RData, self.end_pos = socket.inet_ntoa(data[start_pos: start_pos+4]), start_pos+4

class NSRData(PrettyPrinter):
    def __init__(self, data: bytes, start_pos: int) -> None:
        self.RData, self.end_pos = read_string(data, start_pos)
        
class ResourceRecord(PrettyPrinter):

    def __init__(self, data: bytes, start_pos: int) -> None:
        self.Name, start_pos = read_string(data, start_pos)
        self.Type, self.Class, self.TTL, self.RDLength = struct.unpack(">HHIH", data[start_pos:start_pos+10])
        if self.Type == 2:
            self.RData = NSRData(data, start_pos+10)
        elif self.Type == 1:
            self.RData = ARData(data, start_pos+10)
        else:
            print(self.Type)
        self.end_pos = start_pos+10+self.RDLength

class Message(PrettyPrinter):
    def __init__(self,data) -> None:
        self.header = Header(data)
        self.questions = []
        self.answers = []
        self.authority = []
        self.additional = []
        start_pos = 12
        for _ in range(self.header.QDCount):
            question = Question(data, start_pos)
            start_pos = question.end_pos
            self.questions.append(question)
        for _ in range(self.header.ANCount):
            rr = ResourceRecord(data, start_pos)
            start_pos = rr.end_pos
            self.answers.append(rr)
        for _ in range(self.header.NSCount):
            rr = ResourceRecord(data, start_pos)
            start_pos = rr.end_pos
            self.authority.append(rr)
        for _ in range(self.header.ARCount):
            rr = ResourceRecord(data, start_pos)
            start_pos = rr.end_pos
            self.additional.append(rr)
        

        super().__init__()

msg = Message(data_orig)
print(msg)