"""
Takes a list of jobs with priority
Orders them by priority (high first)
"Places" each on a node (just pick the least-loaded one)

"""
from job import Job
from node import Node
from queue import PriorityQueue
from job_state import JobState

class JobScheduler:
    def __init__(self):
        self.job_queue = PriorityQueue()
        self.nodes = {}

    def schedule_job(self):
        """Scheduling loop"""
        if self.job_queue.empty():
            return None

        item = self.job_queue.get()
        job = item[1] if isinstance(item, tuple) and len(item) == 2 else item

        feasible_nodes = self.filter_nodes(job, self.nodes.values())
        best_node = self.score_nodes(feasible_nodes, job)
        if best_node is None:
            return None

        self.bind_node(job, best_node)
        return job, best_node

    def filter_nodes(self, job, available_nodes):
        """Find nodes that can run this job"""
        feasible_nodes = []
        for node in available_nodes:
            if node.available_cpu >= job.cpu_request and node.available_memory >= job.memory_request:
                feasible_nodes.append(node)
        return feasible_nodes

    def score_nodes(self, feasible_nodes, job):
        """Find most suitable node to run this job"""
        best_node = None
        best_score = float("-inf")

        for node in feasible_nodes:
            cpu_score = node.available_cpu / node.total_cpu if node.total_cpu else 0
            memory_score = node.available_memory / node.total_memory if node.total_memory else 0
            score = cpu_score * 50 + memory_score * 50

            if getattr(job, "data_id", None) is not None and node.has_cached_data(job.data_id):
                score += 10

            if score > best_score:
                best_score = score
                best_node = node

        return best_node

    def bind_node(self, job, best_node):
        """Assign job to node"""
        if best_node is None:
            return False

        best_node.assign_job(job)
        job.state = JobState.RUNNING
        return True
