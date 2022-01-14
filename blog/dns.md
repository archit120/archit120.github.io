---
layout: default_blog
title: Archit - A DNS Dive - Creating a DNS Resolver
description: Hi! I'm Archit. This page attempts to chronicle my experience of creating a DNS resolver
---

## A DNS Dive - Part 1

### Motivation

_Trying to re-re-restart this website. Maybe third time's the charm._

As I talked about in a [previous](mnc.md) post, I really don't like the coursework provided by my university. So I made it a mission to redo all the fundamental CS courses by myself using whatever the best resources I can find on the internet. For the networking part of this endeavour I have decided to take a little different approach. Mostly because I find myself with way too much free time these days. The idea is to do random projects that I design from scratch and give me insight into the topic that I am learning.  

## Goal

The idea is to create a python based program capable of doing address name resolution using root level servers and then following the trail of answers to find the IP address for the requested host. I have decided to go with python because I don't want to deal with debugging using GDB. It's anyway easy to convert the final working python code to C as long as I stick to not using any advanced functionality. For now I'll be using unix UDP sockets but I plan on exploring raw sockets later (should be easy with UDP). 

For this part my goal is to simply handcraft a DNS message, send it and interpret the reply. The target domain being `citadel.com`. 

## How

I am following [RFC1035](https://datatracker.ietf.org/doc/html/rfc1035) that describes DNS but I will be summarizing the key insights needed here. Since DNS is a application layer protocol, usually there's no choice on the transport layer protocol but in this case both UDP and TCP services are available. I have decided to choose UDP because it would be significantly easier to convert this to raw sockets down the line if I wanted. It's also potentially easier to fireoff Wireshark and see what's happening with UDP.


### Message

All communications happen using format called message. The structure for this format is

```
    +---------------------+
    |        Header       |
    +---------------------+
    |       Question      | the question for the name server
    +---------------------+
    |        Answer       | RRs answering the question
    +---------------------+
    |      Authority      | RRs pointing toward an authority
    +---------------------+
    |      Additional     | RRs holding additional information
    +---------------------+
```

Let's look at the sections now. 

### Header

The header is present in all messages. It structure follows - 

```
                                    1  1  1  1  1  1
      0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                      ID                       |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |QR|   Opcode  |AA|TC|RD|RA|   Z    |   RCODE   |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    QDCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    ANCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    NSCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    ARCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
```

Over here the fields and their values are 

 - ID - Any random 16 bit number works. The protocol guarantees that replies to queries will have the same ID. So let's just use `0100h`.
 - QR - `0` for query and `1` for response. We pick `0`.
 - Opcode - `0` for standard query. 
 - TC - Indicates truncation. For us it will be `0`.
 - RD - Recursion flag. We do not want recursion by server and will instead code it manually so set it to `0`. 
 - QDCOUNT - Number of questions. `1`

All of the other fields will be `0` as they are not needed. Finally the header part for our message beomes - 

```
00 00 - ID
00 00 - QR+Opcode+AA+TC+RD+RA+Z+RCODE
00 01 - QDCOUNT
00 00 - ANCOUNT
00 00 - NSCOUNT
00 00 - ARCOUNT
```

### Question

The question is the only extra section in our query message. Its structure is - 

```
                                    1  1  1  1  1  1
      0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                                               |
    /                     QNAME                     /
    /                                               /
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                     QTYPE                     |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                     QCLASS                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
```


 - QNAME - Domain hosts are represented using a sequence of labels. So, `citadel.com` becomes `citadel` and `com`. Further, the data representation of labels in DNS protocol requires that the sequence of labels has the length of the string as the first byte, followed by the string. The final byte must be `0`. 

 - QTYPE - For now, we are only interested `A` type records so this is set to `00 01`.

- QCLASS - We want DNS records from the internet so this value is also `00 01`.

The final query part becomes 
```
07 63 - 7, c
69 74 - i, t
61 64 - a, d
65 6C - e, l
03 63 - 3, c
6F 6D - o, m
00 - termination of QNAME
00 01 - QTYPE, A Records
00 01 - QCLASS, the internet
```

With all that done, the final packet in hex is 
```
000000000001000000000000076369746164656C03636F6D0000010001
```

## Sending the Packet

Before we can send the packet we need to figure out where. [This](https://www.iana.org/domains/root/servers) lists out the root DNS servers. I am choosing the first one with the IP `198.41.0.4` but any should work. Now we need a program to send this packet. 

We could do this using terminal tools but since we wish to eventually make a python program I decided to use Python code to send the packet. This is a simple [script](https://github.com/archit120/DNSWhy/blob/master/manual/dns1.py) that sends the UDP packet, received the output and prints it nicely in hex and ascii. 

```python
import socket
import base64

server = "198.41.0.4"
port = 53

message_hex = "010000000001000000000000076369746164656C03636F6D0000010001"
message_binary = base64.b16decode(message_hex, True)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(message_binary, (server, port))
data, _ = sock.recvfrom(1024)

data = data + b'\0'*(4-len(data)%4) # hack for outut formatting

ascii_str = data.decode("ascii", "replace")
hex_str = base64.b16encode(data).decode("ascii")

for i in range(0, len(hex_str), 4):
    print("{0} {1} | {2} {3}".format(hex_str[i:i+2], hex_str[i+2:i+4], ascii_str[i//2], ascii_str[i//2+1]))
```

The data received back from the server is 
```
01 00 | 
80 00 | �
00 01 |  ☺
00 00 |
00 0D |
00 0E |  ♫
07 63 |  c
69 74 | i t
61 64 | a d
65 6C | e l
03 63 | ♥ c
6F 6D | o m
00 00 |
01 00 | ☺
01 C0 | ☺ �
14 00 | ¶
02 00 | ☻
01 00 | ☺
02 A3 | ☻ �
00 00 |
14 01 | ¶ ☺
61 0C | a ♀
67 74 | g t
6C 64 | l d
...
```

Truncated the rest of the packet for brevity.

## Understanding the Response

### Header
The response structure also follows the standard message format. So we can first interpret the header. 

```
01 00 - ID matches the one we sent
80 00 - QR+Opcode+AA+TC+RD+RA+Z+RCODE
00 01 - Query Count
00 00 - Answer Count
00 0D - 13 Authority RR
00 0E - 14 Additional RR
```

To understand the third and forth bytes we need to blow it up to binary. `80 00` in binary is - 

```
                                    1  1  1  1  1  1
      0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |QR|   Opcode  |AA|TC|RD|RA|   Z    |   RCODE   |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
      1  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0
```

So we can clearly see the QR is `1` and everything else is `0`. QR being `1` means this is a response as expected and the rest of the fields indicate standard query, no recursion and no errors. `RCODE` is `0` which means no errors.

### Question

Identical to the original question we sent.

### Resource Record

Before we can interpret Authority and Additional sections we need to look at RR formats and message compression.

```
                                    1  1  1  1  1  1
      0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                                               |
    /                                               /
    /                      NAME                     /
    |                                               |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                      TYPE                     |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                     CLASS                     |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                      TTL                      |
    |                                               |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                   RDLENGTH                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--|
    /                     RDATA                     /
    /                                               /
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
```


The fields are -

 - NAME - Name of the node for which the record exists. 
 - TYPE - Similar to QTYPE. For this project we need `A`, `NS` and `CNAME` records which have the values `1` , `2` and `5`.
 - CLASS - Should always be `1` for internet
 - TTL - Standard 32 bit TTL with big-endian encoding. `0` means no caching
 - RDLENGTH - 16 bit integer containing length of RDATA
 - RDATA - Associated data with the RR. We consider 3 formats.

### Message Compression

All `NAME` data fields can be compressed using pointers. The method to interpret this compression is pretty simple. Any label that start with `11` in the first two higher order bits represents compression. The next 6 bits are a pointer to where the actual label already exists in the packet. For example - 

```

       +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    20 |           1           |           F           |
       +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    22 |           3           |           I           |
       +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    24 |           S           |           I           |
       +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    26 |           4           |           A           |
       +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    28 |           R           |           P           |
       +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    30 |           A           |           0           |
       +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

       +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    40 |           3           |           F           |
       +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    42 |           O           |           O           |
       +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    44 | 1  1|                20                       |
       +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
```
The `NAME` starting at `40` is `FOO.F.ARPA`.

### CNAME RDATA

```
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    /                     CNAME                     /
    /                                               /
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
```

 - CNAME - The queried for name is an alias for the name present in this field

### NS RDATA

```
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    /                   NSDNAME                     /
    /                                               /
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
```
- NSDNAME - The returned domain name should be an authoritative nameserver for the queried domain. We will have to recusrively query the given name-server.

### A RDATA

```
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    ADDRESS                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
```

- ADDRESS - 32 bit IP address for the domain name.

### Scripting Time

With all that out of the way we can finally start interpreting the entire packet. Because the response packet is very big I didn't want to go breaking it apart byte by byte. This [python script](https://github.com/archit120/DNSWhy/blob/master/manual/dns2.py) is an extension of the previous one and does just that. The pretty-printed output is 

```
Message:
    header: Header:
        ID: 256
        QDCount: 1
        ANCount: 0
        NSCount: 13
        ARCount: 14
        QR: True
        Opcode: 0
        AA: False
        TC: False
        RD: False
        RA: False
        Z: 0
        RCODE: 0
    questions: [Question:
        QName: citadel.com
        QType: 1
        QClass: 1
        end_pos: 29]
    answers: []
    authority: [ResourceRecord:
        Name: com
        Type: 2
        Class: 1
        TTL: 172800
        RDLength: 20
        RData: NSRData:
            RData: a.gtld-servers.net
            end_pos: 61
        end_pos: 61, ResourceRecord:
        ...
    additional: [ResourceRecord:
        Name: a.gtld-servers.net
        Type: 1
        Class: 1
        TTL: 172800
        RDLength: 4
        RData: ARData:
            RData: 192.5.6.30
            end_pos: 269
        end_pos: 269, ResourceRecord:
        ...
        Name: a.gtld-servers.net
        Type: 28
        Class: 1
        TTL: 172800
        RDLength: 16
        end_pos: 489]
```

### Interpretation

The answers section is empty so the queried name-server does not know where `citadel.com` is. However, it does tell us other information that maybe useful. Namely these are `NS` type records for `.com` top-level-domain. The additional part of the message also contains the `A` and `AAAA` records for these name-servers. So now we can query one of these nameservers. To proceede further we will need recursion and that's the topic for [part - 2](dns2).