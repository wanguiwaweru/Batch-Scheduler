from job_state import JobState


class Job:
    def __init__(self, name, cpu_request, memory_request, state: JobState, data_id=None):
        self.name = name
        self.cpu_request = cpu_request
        self.memory_request = memory_request
        self.state = state
        self.data_id = data_id
