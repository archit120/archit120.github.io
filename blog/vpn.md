---
layout: default_blog
title: Archit - A DNS Dive - Creating a DNS Resolver
description: Hi! I'm Archit. This page attempts to chronicle my experience of creating a DNS resolver
---

## Write your own VPN _(sort of)_

### Decisions 
 - Golang
 - Avoid encryption and decyption overhead
 - 1 to 1 tunnel. NAT router on the client end

### Resources 
 - https://nsl.cz/using-tun-tap-in-go-or-how-to-write-vpn/ - Go tunnel usage
 - https://github.com/songgao/water - tunnel library
 - https://github.com/vishvananda/netlink/tree/main - set ip * commands from code


TCP message - `<datagram length><datagram>`

on client side read dataframes from TUN adapter, enclose in this format and send.
for incoming frames from net, do nothing pass into raw socket as is.

on server side, modify ip datagram src and resend.
received packets modify ip datagram dst and resend

### To figure out 
 - how to send packets on internet? (this connection does not use defualt routing?)


### extras
 - TLS support. Or at least pretend TLS