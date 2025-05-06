#!/usr/bin/env python2
"""NAO side TCP server: speaks every string received and keeps the socket open."""

import socket
import sys
import traceback
from naoqi import ALProxy

LISTEN_IP   = '0.0.0.0'
LISTEN_PORT = 10000
ROBOT_IP    = '169.254.242.81'   
ROBOT_PORT  = 9559
BUFF_SIZE   = 4096               

def main():
    try:
        tts = ALProxy('ALTextToSpeech', ROBOT_IP, ROBOT_PORT)
    except Exception as e:
        print('ERROR: cannot reach ALTextToSpeech →', e)
        sys.exit(1)

    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    try:
        srv.bind((LISTEN_IP, LISTEN_PORT))
        srv.listen(1)
    except Exception as e:
        print('ERROR: bind/listen failed →', e)
        sys.exit(1)

    print('NAO server listening on %s:%d' % (LISTEN_IP, LISTEN_PORT))

    while True:
        conn, addr = srv.accept()
        print('Client connected from', addr)
        try:
            while True:
                try:
                    data = conn.recv(BUFF_SIZE)
                except socket.error as se:
                    print('Socket error:', se)
                    break

                if not data:                      
                    print('Client disconnected')
                    break

                text = data.decode('utf-8').strip()
                print('→', text)
                try:
                    tts.say(text)
                except Exception:
                    traceback.print_exc()

                conn.sendall('Spoken'.encode('utf-8'))
        finally:
            conn.close()
            print('Ready for the next client…')

if __name__ == '__main__':
    main()
