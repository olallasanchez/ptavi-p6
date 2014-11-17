#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import SocketServer
import sys
#import os.path

class EchoHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            Info = line.split(' ')
            Metodo = Info[0]
            Metodo = Metodo.upper()
            Lista_Metodos = ["INVITE", "BYE", "ACK"]
            if Metodo == 'INVITE':
                print line
                Envio = 'SIP/2.0 100 Trying\r\n\r\n'
                Envio += 'SIP/2.0 180 Ring\r\n\r\n'
                Envio += 'SIP/2.0 200 OK\r\n\r\n'
                self.wfile.write(Envio)
            elif Metodo == 'ACK':
                print 'RTP......'
            elif Metodo == 'BYE':
                print line
                Envio = 'SIP/2.0 200 OK\r\n\r\n'
                self.wfile.write(Envio)
            elif not Metodo in Lista_Metodos:
                if line != '':
                    Envio = 'SIP/2.0 405 Method Not Allowed\r\n\r\n'
                    self.wfile.write(Envio)
            else:
                Envio = 'SIP/2.0 400 Bad Request\r\n\r\n'
                self.wfile.write(Envio)
            # Si no hay más líneas salimos del bucle infinito
            if not line:
                break

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    if len(sys.argv) == 4:
        #if os.path.exists(sys.argv[3]):
        serv = SocketServer.UDPServer(("", int(sys.argv[2])), EchoHandler)
        print "Listening..."
        serv.serve_forever()
    else:
        print 'Usage: python server.py IP port audio_file'
        #COMPROBAR EL FICHERO DE AUDIO
