import pandas
import time
import threading

from PIDs.pid_factory import PIDFactory

class EngineSimulation:

    def __init__(self):
        self.simulation_ready = False
        self.__simulation_data = {}
        self.__simulation_timer = None

    def initalize_simulation(self, simulation_data):
        pid_table, channel_info = self.__parse_simulation_data(simulation_data)
        if not self.simulation_ready:
            if pid_table is None:
                print('ERROR: Failed to initialize engine simulation')
                return False
            else:
                self.__load_simulation_data(pid_table, channel_info)
                pass
        else:
            print('ERROR: Simulation is already running')
            return False
        return True

    def __parse_simulation_data(self, simulation_data_csv):
        index = 0
        with open(simulation_data_csv, 'r') as f:
            line = f.readline()
            index += 1
            if not line == 'HP Tuners CSV Log File\n':
                print('ERROR: Invalid simulation data provided')
                return None
            print('Simulation Data: Header OK')
            for line in f:
                index += 1
                if line == '[Log Information]\n':
                    print('Simulation Data {}'.format(f.readline()))
                    print('Simulation Data {}'.format(f.readline()))
                    index += 2
                if line == '[Channel Information]\n':
                    # print('Simulation Data Channel Information starts at {}'.format(index))
                    channel_information = pandas.read_csv(simulation_data_csv, skiprows=index, nrows=2)
                if line == '[Channel Data]\n':
                    # print('Simulation Data Channel Data starts at {}'.format(index))
                    channel_data = pandas.read_csv(simulation_data_csv, skiprows=index, header=None, index_col=0)
                    channel_data.columns = channel_information.columns[1:]
                    break
        return channel_data, channel_information

    def __load_simulation_data(self, pid_table, channel_info):
        # Get the last time in the simulation data and set that as the roll over time on the simulation timer
        self.__simulation_timer = SimulationTimer(pid_table.index[-1])
        pid_table_dict = pid_table.to_dict()

        # Load the PID channels
        for pid_id in channel_info:
            pid_id_int = int(pid_id, base=10)
            pid = PIDFactory.get_pid_by_id(
                pid=pid_id_int,
                pid_data=pid_table_dict[pid_id] if pid_id in pid_table_dict else None,
                sim_timer=self.__simulation_timer)
            if pid is None:
                continue
            self.__simulation_data[pid_id_int] = pid
        return True

    def start_simulation(self):
        self.__simulation_timer.start_simulation_timer()

    def stop_simulation(self):
        self.__simulation_timer.start_simulation_timer()

    def get_value_for_pid(self, pid):
        return self.__simulation_data[pid].get_value() if pid in self.__simulation_data else None

    def get_response_for_pid(self, pid):
        return self.__simulation_data[pid].get_response() if pid in self.__simulation_data else None

class SimulationTimer:

    def __init__(self, roll_over_time_s):
        self.__start_simulation_time = None
        self.__roll_over_time = roll_over_time_s
        self.__keeper_thread = threading.Thread()

    def start_simulation_timer(self):
        self.__start_simulation_time = time.time()
        self.__keeper_thread = threading.Thread(target=self.__time_keeper).start()

    def stop_simulation_timer(self):
        self.__keeper_thread.join()
        self.__start_simulation_time = None

    def get_simulation_time(self):
        return time.time() - self.__start_simulation_time

    def __time_keeper(self):
        while True:
            if self.get_simulation_time() > self.__roll_over_time:
                print('INFO: Simulation rolling over')
                self.__start_simulation_time = time.time()
            time.sleep(1 / 1000)  # millisecond sleep





