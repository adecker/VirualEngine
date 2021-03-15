
from simulation.engine_simulation import EngineSimulation

class OBDIISimulation:
    def __init__(self, address='localhost', port=1320):
        self._address = address
        self._port = port
        self.__simulation_data = None
        self.__engine = EngineSimulation()
        self.simulation_ready = False

    def prepare_simulation(self, data):
        self.__simulation_data = data
        if self.__engine.initalize_simulation(simulation_data=data):
            print('Simulation data loaded into engine')

    def start_simulation(self):
        self.__engine.start_simulation()

    def stop_simulation(self):
        self.__engine.stop_simulation()




