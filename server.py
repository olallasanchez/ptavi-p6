#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import SocketServer
import sys


class EchoHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            if not line:
                break
            print line
            Info = line.split(' ')
            Metodo = Info[0]
            if Metodo == 'INVITE':
                Envio = 'SIP/2.0 100 Trying\r\n\r\n'
                Envio += 'SIP/2.0 180 Ring\r\n\r\n'
                Envio += 'SIP/2.0 200 OK\r\n\r\n'
                self.wfile.write(Envio)
            elif Metodo == 'ACK':
                print 'OLALLA ACK'
            elif Metodo == 'BYE':
                print 'OLALLA BYE'

            # Si no hay más líneas salimos del bucle infinito
            

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = SocketServer.UDPServer(("", int(sys.argv[2])), EchoHandler)
    print "Listening..."
    serv.serve_forever()
