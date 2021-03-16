from PIDs.base_pid import PID


class EngineSpeed(PID):
    def __init__(self, pid_data, simulation_timer):
        super(EngineSpeed, self).__init__(0x0C, pid_data, simulation_timer)

    def update_response(self):
        response_bytes = int(self.get_value() * 4).to_bytes(length=2, byteorder='big')
        self._response.clear()
        self._response.append(self._pid)
        self._response.append(response_bytes[0])
        self._response.append(response_bytes[1])
