

# 

I recently had the requirement for a very simple VPN setup with a server-client setup such that internet for the client is routed through the server's connection. Usually this can be achieved through one of the countless VPN protocols like OpenVPN or WireGuard. However, for my situation neither of these were really suitable. The firewall on the client's internet prevents outgoing connections of anything except TCP ports 80 and 443. This ruled out every mainstream VPN protocol except OpenVPN that does work over TCP. Finally, OpenVPN is pretty slow and does a lot of nice-to-haves that I didn't need so I decided to write my own version.

## TAP/TUN interface

The first thing we need to do for a working internet tunnel is establish some way to create a virtual network interface from software. Conveniently, Linux supports this using tap/tun interfaces which are layer 2 and layer 3 network interfaces respectively. The OS treats them as any other network interface but also provides a simple way to read and write packets to these interfaces. 

A high-level overview at this point can be established. All we need to do is redirect the packets destined for the internet to our own interface, read all packets arriving here, send them to the server using the actual interface that provides internet connectivity. At the server end, the reverse happens which is receiving packets from client's TCP stream, and getting it to the internet somehow.

Getting packets to the internet is a little convoluted. The VPN tunnel will create  a local network so there is some address associated with connected clients. When the server dumps a packet received from any of the clients to its actual physical interface it cannot do so without any modifications because the IP address associated with these clients is not the same as the IP address of the server's physical interface. 

At this point, we need to look into NAT. This is another can of worms in itself but the tl;dr is that setting up NAT rules and ip forwarding on Linux will make the server act as a router. When correctly configured, packets received on any interface destined for the internet will be routed to the physical interface and appropriate modifications needed for IP translation will be automatically done.

There are n major things to do for writing your own basic VPN -

1. Create a TAP/TUN interface on both the server and client depending on whether you want an L2 or L3 VPN. 
2. Establish a UDP/TCP connection between the two. When doing this we want to create a route exception for the server's IP  on the client otherwise packets to the VPN server will get routed through the VPN aswell resulting in a loop.
3. Set up NAT rules on the server to send packets received on the TAP/TUN interface through the physical interface.
4. Set up ip routes on the client to send all packets to the virtual interface.
5. Use the established UDP/TCP connection to send all packets read on the interface and write all packets received from the connection.


For 4. we need to setup the special routes using

```
ip r add 0.0.0.0/1 dev tun0 via ...
ip r add 128.0.0.0/1 dev tun0 via ...
```

These work because of longest prefix matching rules for routing. The default route for internet connectivity will be `0.0.0.0/0` so these rules while covering all IP addresses match one additional bit and will therefore be the preferred route. 

A basic implementation in Golang using these principles is at my github.