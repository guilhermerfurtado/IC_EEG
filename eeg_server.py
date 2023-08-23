#!/usr/bin/env python3
#
# https://docs.python.org/3.5/library/socketserver.html#socketserver-tcpserver-example
#
import pandas as pd
import numpy as np
import socketserver
import time
import icelera


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def signal(self, freq_sample=512, time_sample=1, n_waves=48, amplitude=100):
        """
        Signal generator calculate 20 senoid waves with
        frequency sinal ranging from 1Hz to 80Hz
        Used in server signal generator
        """
        timesample = np.linspace(0, time_sample, freq_sample * time_sample)
        val = amplitude * (np.array(
                [np.sin(2*np.pi*fs*timesample) for fs in np.arange(1, n_waves+1)]))
        return pd.DataFrame(val.T)

## a parte acima não consta no código original da documentação socketServer
## foi algo adicionado pelo Rodrigo Prior

    def handle(self):
        # connection accepted
        addr = self.client_address
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print('Client ' + addr[0] + ':' + str(addr[1]) + ' wrote:', '\n', self.data)
        # check to initialize data Sending
        if self.data == b'w\xeeUw\xeeC\x01\x01\x00\x01\x01\x00\x01\x01\x00\x01\x00\x00\x01\x00\x00\x01\x00\x00\x01\x00\x00\x01\x00\x00\x01\x01\x00\x01\x01\x00\x01\x01\x00\x01\x00\x00\x01\x00\x00\x01\x00\x00\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00':
            print("Ok. Sending electrode data...")
            s = self.signal(n_waves=11)
            # initiate signal data sending
            self.request.send(icelera.responses['memory_card'])
            self.request.send(icelera.responses['channel_list'])
            while True:
                for index, col in s.iterrows():
                    data = icelera.signals['channel_header'] + s.loc[index].astype(np.intc).values.tobytes()
                    # print(len(data))
                    self.request.sendall(data)
                    # self.request.send(16*(bytearray(b'U\xaaU\xaa') + 52*bytearray(b'\x01')))
                    # sleep to simulate data throughput (512Hz)
                    time.sleep(1./512)

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
    print('Socket created')

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
        print('Shutdown socket server')
