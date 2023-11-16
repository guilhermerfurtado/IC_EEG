#!/usr/bin/env python3
import argparse
import numpy as np
import pandas as pd
import time
import socket
import struct
import re
import os
import sys
nome = 'T2_Franco16'

#Para executar o programa escreva na prompt python icelera.py client
signals = {
    'start': bytearray([0x77, 0xEE, 0x55]),
    'memory_card': bytearray([0x77, 0xEE, 0x47, 0x37]),
    'channel_list': bytearray([0x77, 0xEE, 0x43]) + 20*bytearray([0x01]),
    'security':  bytearray([0x77, 0xEE, 0x74]),
    'channel_header': bytearray([0x55, 0xAA, 0x55, 0xAA, 0x35, 0x00, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00])
}
# TODO: cleanup this in the future
responses = {
    'memory_card': bytearray([0x55, 0x5A, 0x55, 0x5A, 0x47, 0x3D, 0x30]),
    'channel_list': bytearray([0x55, 0x5A, 0x55, 0x5A, 0x43]) + 20*bytearray([0x01]),
    }

HEADER_WORD = b'U\\xaaU\\xaa'


class iblue(object):

    def __init__(self):
       # self.host = '172.31.1.201' #IP conectado na porta Ethernet
       # self.host = '192.168.1.103' #IP do P                                               C
        self.host = '192.168.5.10' #IP que veio no código
        self.port = 9000
        self.group = ['eeg']
        self.channels = []

    def channel_selector(self, group):
        """
        Function that return channel list bytearray
        Options:
          group = ['eeg', 'emg', 'poli', 'eeg+', 'ecg', 'cpap']
        Return:
          channel_bytearray: icelera head + 0 or 1 for every channel
        Usage:
          channel_bytearray = channel_selector(group=['eeg','eeg+'])
        """
        df = pd.read_csv(
            os.path.join(os.path.dirname(__file__), 'channel_list.txt'),
            index_col=0)
        df.status = 0  # zero to all status
        df.loc[df.group.isin(group), 'status'] = 1  # ones to selected
        return bytearray([0x77, 0xEE, 0x43])+bytearray(df.status.astype('byte'))

    def channel_names(self, channel_bytes):
        """
        Function that return channel list names
        Options:
          channel_bytes: tuple of bytes from selected channels
            read from struct.unpack.
            channel_bytes = (b'\x01',b'\x01',b'\x00',b'\x01',...)
        Return:
          List of enabled channel names
        Usage:
          channel_name = channel_names(channel_bytes)
        """
        df = pd.read_csv(
            os.path.join(os.path.dirname(__file__), 'channel_list.txt'),
            index_col=0)
        #df.status = 0  # zero to all status
        #df.status = [int(bytes.hex(i)) for i in channel_bytes] + 13*[0]
        return df.channel[df.status == 1].tolist()

    def channel_convrate(self, group):
        """
        Function that return channel list array with conversion rate from AD to Volt.
        Options:
          group = ['eeg', 'emg', 'poli', 'eeg+', 'ecg', 'cpap']
        Return:
          Numpy array with conversion rate from AD to Volt for each channel.
        Usage:
          channel_bytearray = channel_convrate(group=['eeg','eeg+'])
        """
        df = pd.read_csv(
            os.path.join(os.path.dirname(__file__), 'channel_list.txt'),
            index_col=0)
        df.status = 0  # zero to all status
        df.loc[df.group.isin(group), 'status'] = 1
        return np.array(df.conv_factor[df.status == 1].tolist())

    def socket_client(self):
        """
        Create socket connection to hardware and return an iterator.
        Return:
            Iterator with a tuple of channel values
        """
        channel_bytearray = self.channel_selector(self.group)
       # print("channel", channel_bytearray)
        convfactor_array = self.channel_convrate(self.group)
        try:
            # Create a socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                # Connect to server and send data
                sock.connect((self.host, self.port))
                sock.send(signals['start'])
                sock.send(channel_bytearray)
                # forget icelera messaging and make my own header
               # print ("completo", struct.unpack('48c', self.channel_selector(self.group)))
              #  print("novo: ", str(self.channel_selector(self.group)[:3]))
              #  print("selecionado", self.channel_selector(self.group)[3:-13])
                print(len(self.channel_selector(self.group)[3:-13]))
                testando = self.channel_selector(self.group)[3:-13]
                header = struct.unpack("!%sH" % (len(testando) // 2), testando)
              #  print('header', header)
                # return the channel names
                self.channels = self.channel_names(header)
                # regex parser step
              #  fmt = '8s' + 'h'*sum([int(bytes.hex(i)) for i in header])
                fmt = '8s' + 'h'*23
              #  print('fmt', fmt)
                inicio_execucao = time.time()
                run = 1
                while run:
                    # split network frames
                    frames = re.split(HEADER_WORD, sock.recv(4096))
                    #frames = re.split(b'U\\xaaU\\xaa', sock.recv(4096))
                    #frames = sock.recv(4096)
                    #print("frames", frames[1])
                    #print(frames)
                    #print(np.frombuffer(frames, dtype=np.int16))
                    #exit()
                    # parse frame and remove first column trash and clean icelera erroneous frames
                    #data = [struct.unpack(fmt, i)[1:] for i in frames]
                   # valores = [np.int16(val) for val in frames]
                    #print(valores)
                    data = [struct.unpack(fmt, i)[1:] for i in frames if len(i) == struct.calcsize(fmt)]
                   # print(data)
                    #print("data:", data[1])
                    #data = struct.unpack(29*'h', frames)
                    #print (data[:2])
                    for packet in data:
                        # return list single frame from network package
                        yield list(np.array(packet)/convfactor_array)
                
                    if (time.time() - inicio_execucao >= 8 and time.time() - inicio_execucao <= 9.5):
                        print("***********AGORA***********")

                    if (time.time() - inicio_execucao >= 24 and time.time() - inicio_execucao <= 25.5):
                        print("+++++++++++MOVER++++++++++++")
            
                    if (time.time() - inicio_execucao >= 42 and time.time() - inicio_execucao <= 43.5):
                        print("-----------SINAL-----------")
                    if time.time() - inicio_execucao >= 57:
                        run = 0
        finally:
            print("Tempo de execução:", time.time() - inicio_execucao, "segundos")
            sock.close()


def main():
    """ Parse command line options """
    parser = argparse.ArgumentParser(
        prog='icelera',
        description='Series of functions to work with icelera nanoEEG.',
        usage='python3 icelera'
    )

    subparsers = parser.add_subparsers(help='commands', dest='command')
    socketclient_parser = subparsers.add_parser(
        'client',
        help='start socket connection to icelera hw and display stream')
    socketclient_parser.add_argument(
        '-o', action='store', default=f'{nome}.csv',
        help='Output Filename (default: {nome}.csv)')
    socketclient_parser.add_argument(
        '--ip', action='store', default='192.168.5.10',
        help='iCelera Nano EEG hardware address (default: 192.168.5.10)')
    socketclient_parser.add_argument(
        '--port', action='store', type=int, default=9000,
        help='iCelera Nano EEG hardware port (deafult: 9000)')
    socketclient_parser.add_argument(
        '--group', action='store', nargs='*', default=['eeg'],
        help="""iCelera Nano EEG channel group port (default: eeg).
        Options: eeg emg poli eeg+ ecg cpap (can also be combined: eeg emg).
        Refer to file ./channel_list.txt""")

    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
    elif args.command == 'client':
        print('Send data:')
        print('host:', args.ip, 'port:', args.port, 'file:',
              args.o, 'group:', args.group)
        print('Press CTRL+c to stop.')
        data_bufer = []
        try:
            # call and define class parameters
            ic = iblue()
            ic.host = args.ip
            ic.port = args.port
            ic.group = args.group
            data = ic.socket_client()
            # iterate data from iblue
            for d in data:
                data_bufer.append(d)
            
            df_csv = pd.DataFrame(data_bufer, columns=ic.channels)
            df_csv.to_csv(args.o, index=False)
            print('File saved:', args.o)
            

            sys.exit()

        except KeyboardInterrupt:
            #print("data_buffer", data_bufer[:2])
            #print(ic.channels)
            # convert and save data to disk
            pass
            

        

if __name__ == "__main__":
    main()
