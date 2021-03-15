import time
from simulation.obd2_simulation import OBDIISimulation

obd_server = OBDIISimulation()
obd_server.prepare_simulation('simulation_data/1.csv')
obd_server.start_simulation()

while True:
    pass