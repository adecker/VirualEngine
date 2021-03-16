
class PID:

    def __init__(self, pid, pid_data, simulation_timer):
        self._pid = pid
        self._response = []
        self.__value = 0
        self.__pid_data = pid_data
        self.__simulation_timer = simulation_timer

    def update_response(self):
        """A complete response will usually consist of the first two bytes
        representing the response code, and up to four bytes being used to relay the
        value. We drop the mode byte of the response header because the OBD-II server will tag that
        on automatically for us. We do this because a device can request multiple PIDs in one request
        so if we added the mode response byte to every message then the response would be invalid"""
        pass

    def get_response(self):
        self.update_response()
        return self._response

    def set_value(self, value):
        """Sets the value of the underlying PID. This value will be used to calculate the response
        when get_response() is called"""
        self.__value = value
        self.update_response()

    def get_value (self):
        if self.__pid_data is None and self.__simulation_timer is None:
            return self.__value
        else:
            sim_time = self.__simulation_timer.get_simulation_time()
            return self.__pid_data[sim_time] if sim_time in self.__pid_data \
                else self.__pid_data[min(self.__pid_data.keys(), key=lambda k: abs(k-sim_time))]





