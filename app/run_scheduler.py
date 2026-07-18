from job import Job
from node import Node
from scheduler import JobScheduler
from job_state import JobState


def main():
    scheduler = JobScheduler()

    scheduler.nodes = {
        "node1": Node(
            "node1", total_cpu=8, total_memory=16000, cached_data=["dataset-A"]
        ),
        "node2": Node("node2", total_cpu=16, total_memory=32000, cached_data=[]),
    }

    jobs = [
        (
            1,
            Job(
                "job-a",
                cpu_request=4,
                memory_request=4000,
                state=JobState.PENDING,
                data_id="dataset-A",
            ),
        ),
        (
            2,
            Job(
                "job-b",
                cpu_request=8,
                memory_request=12000,
                state=JobState.PENDING,
                data_id=None,
            ),
        ),
    ]

    for priority, job in jobs:
        scheduler.job_queue.put((priority, job))

    while not scheduler.job_queue.empty():
        result = scheduler.schedule_job()
        if result is None:
            print("No feasible node found for the next job.")
            break

        job, best_node = result
        print(f"Assigned {job.name} to {best_node.name}")
        print(
            f"  {best_node.name} available_cpu={best_node.available_cpu} available_memory={best_node.available_memory}"
        )
        print(f"  job state={job.state.name}\n")


if __name__ == "__main__":
    main()
