#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

# Cliente UDP simple.
if len(sys.argv) == 3:
    IP_Puerto = sys.argv[2].split(':')
    Correo = IP_Puerto[0]
    Puerto = IP_Puerto[1]
    Correo_Trocea = Correo.split('@')
    Metodo = sys.argv[1].upper()

    # Dirección IP del servidor.
    SERVER = Correo_Trocea[1]
    PORT = int(IP_Puerto[1])

    # Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.connect((SERVER, PORT))

    # Contenido que vamos a enviar
    try:
        LINE = Metodo + ' sip:' + IP_Puerto[0] + ' SIP/2.0\r\n\r\n'
        my_socket.send(LINE)
        data = my_socket.recv(1024)
        print "Enviando: " + LINE
    except socket.error:
        print 'Error: No server listening at ' + Correo_Trocea[1] + ' port ' + IP_Puerto[1]
        raise SystemExit


    print 'Recibido -- ', data
    if Metodo == 'INVITE':
        LINE = 'ACK sip:' + IP_Puerto[0] + ' SIP/2.0\r\n\r\n'
        my_socket.send(LINE)

    # Cerramos todo
    my_socket.close()
    print "Fin."
else:
    print 'Usage: python client.py method receiver@IP:SIPport'
