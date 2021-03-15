from PIDs.Mode01.Other.engine_speed import EngineSpeed


class PIDFactory:

    @staticmethod
    def get_pid_by_id(pid, pid_data, sim_timer ):
        if pid == 0x0C:
            return EngineSpeed(pid_data=pid_data, simulation_timer=sim_timer)
        else:
            print("WARNING: No PID definition found for ID {}".format(hex(pid)))
            return None
