import sys
import subprocess
import os
import threading

from socket import socket
from simulation.engine_simulation import EngineSimulation


class OBDIISimulation:
    def __init__(self, address='localhost', port=1320):
        self.simulation_ready = False
        self._address = address
        self._port = port
        self.__simulation_data = None
        self.__engine = EngineSimulation()
        self.__working_dir = os.path.dirname(os.path.abspath(__file__))
        self.__server = threading.Thread()

    def prepare_simulation(self, data):
        self.__simulation_data = data
        if self.__engine.initalize_simulation(simulation_data=data):
            print('Simulation data loaded into engine')

    def start_simulation(self):
        self.__engine.start_simulation()
        self.__server = threading.Thread(target=self.__start_server).start()

    def stop_simulation(self):
        self.__engine.stop_simulation()

    def __start_server(self):
        s = socket()
        s.bind((self._address, self._port))
        s.listen(2)

        subprocess.Popen([sys.executable, self.__working_dir + '\Shell.py', self._address, str(self._port)])

        c, addr = s.accept()
        print('INFO: Accepted connection from {}'.format(addr))
        while True:
            try:
                data = c.recv(16).decode('utf-8')
                data = str.replace(data, '\r','').lower().split(sep=' ')
                # print('INFO: Received Request: {}'.format(data))
                if data[0] == '01' or data[0] == '0x01':
                    # print('INFO: Requesting Mode: 1 PID: {}'.format(data[1]))
                    response = self.__engine.get_response_for_pid(int(data[1],base=16))
                    c.send(str.encode('NO DATA') if response == 'NO DATA' else str.encode('41 ' +
                                                                                          ''.join('{:02x} '.format(x)
                                                                                                  for x in response)))
                else:
                    c.send(str.encode('NO DATA'))
            except:
                print('ERROR: Failed to parse byte string')
                continue






