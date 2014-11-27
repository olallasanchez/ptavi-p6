#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import SocketServer
import sys
import os


class EchoHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        self.wfile.write("Hemos recibido tu peticion")
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            METHODLIST = ['INVITE', 'ACK', 'BYE']
            line = self.rfile.read()
            print "El cliente nos manda " + line

            # Si no hay más líneas salimos del bucle infinito
            if not line:
                break
            else:
                print line
                wordlist = line.split(' ')
                METHOD = wordlist[0]
                METHOD = METHOD.upper()
                IP_Cliente = str(self.client_address[0])
                if not METHOD in METHODLIST:
                    print "Enviando: SIP/2.0 405 Method Not Allowed"
                    self.wfile.write('SIP/2.0 405 Method Not Allowed\r\n')
                    break
                if METHOD == 'INVITE':
                    print "Enviando: SIP/2.0 100 Trying"
                    self.wfile.write('SIP/2.0 100 Trying\r\n')
                    print "Enviando: SIP/2.0 180 Ringing"
                    self.wfile.write('SIP/2.0 180 Ringing\r\n')
                    print "Enviando: SIP/2.0 200 OK"
                    self.wfile.write('SIP/2.0 200 OK\r\n')
                elif METHOD == 'ACK':
                    # aEjecutar es un string con lo
                    # que se ha de ejecutar en la shell
                    aEjecutar = './mp32rtp -i ' + IP_Cliente + ' -p 23032 < '
                    aEjecutar += SONG
                    print "Vamos a ejecutar", aEjecutar
                    os.system(aEjecutar)
                elif METHOD == 'BYE':
                    print "Enviando: SIP/2.0 200 OK"
                    self.wfile.write('SIP/2.0 200 OK\r\n')


if __name__ == "__main__":

    try:
        IP = sys.argv[1]
        PORT = sys.argv[2]
        SONG = sys.argv[3]
        # comprobamos que existe song
        if not os.access(SONG, os.F_OK):
            print('Usage: python server.py IP port audio_file')
            raise SystemExit
    except IndexError:
        print('Usage: python server.py IP port audio_file')
        raise SystemExit
    except ValueError:
        print('Usage: python server.py IP port audio_file')
        raise SystemExit
    # Creamos servidor de eco y escuchamos
    serv = SocketServer.UDPServer(("", int(PORT)), EchoHandler)
    print "Listening..."
    serv.serve_forever()
