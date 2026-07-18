class Node:
    def __init__(self, name, total_cpu, total_memory, cached_data=None):
        self.name = name
        self.total_cpu = total_cpu
        self.total_memory = total_memory
        self.used_cpu = 0
        self.used_memory = 0
        self.cached_data = set(cached_data or [])

    @property
    def available_cpu(self):
        return self.total_cpu - self.used_cpu

    @property
    def available_memory(self):
        return self.total_memory - self.used_memory

    def has_cached_data(self, data_id):
        return data_id is not None and data_id in self.cached_data

    def assign_job(self, job):
        self.used_cpu += job.cpu_request
        self.used_memory += job.memory_request
