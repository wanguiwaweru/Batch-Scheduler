# Job Scheduler
This job scheduler is an implementation of a batch job scheduling system. It takes a list of jobs with their respective priorities and allocates them to available nodes in a cluster based on their resource requirements.


Scheduler allocates jobs to available clusters based on their requirements such as GPU, CPU, and memory. It ensures that jobs are distributed efficiently across the nodes to optimize resource utilization and minimize job completion time. The scheduler also monitors the status of each node and can reallocate jobs if a node becomes overloaded or fails.

# Scheduler Workflow
┌─────────────────────────────────┐
│ Job Queue (Priority ordered)    │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│ FILTER PHASE                    │
│ - Enough resources              │
│ - Node affinity                 │     
│ → Output: Feasible nodes        │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│ SCORE PHASE                     │
│ - Bin-packing score             │
│ - Spread score                  │
│ - Image locality score          │
│ → Output:Ranked nodes->best node│
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│ SELECT & BIND                   │
│ Pick highest-scoring node       │
│ Assign job to node              │
└─────────────────────────────────┘

## Scheduler design
This scheduler implements a three-phase placement flow in `app/scheduler.py`.

### Phase 1: Filter
`JobScheduler.filter_nodes()` rejects any node that cannot satisfy a job's resource request:
- `node.available_cpu >= job.cpu_request`
- `node.available_memory >= job.memory_request`

Nodes track resource usage in `app/node.py` with:
- `total_cpu`, `total_memory`
- `used_cpu`, `used_memory`
- computed properties `available_cpu` and `available_memory`

### Phase 2: Score
`JobScheduler.score_nodes()` ranks feasible nodes using available capacity and locality.
The current score is:
- `cpu_score = available_cpu / total_cpu`
- `memory_score = available_memory / total_memory`
- `score = cpu_score * 50 + memory_score * 50`
- `+10` if the node already has the job's `data_id` cached

This makes the scheduler prefer nodes with more free capacity and a small bonus for data locality.

### Phase 3: Bind
`JobScheduler.bind_node()` assigns the job to the selected node by:
- updating node usage via `best_node.assign_job(job)`
- setting `job.state = JobState.RUNNING`

### Running the scheduler
A sample entrypoint is available in `app/run_scheduler.py`.
Run it from the app folder with:
```powershell
cd c:\Users\user\Desktop\batch-scheduler\app
python run_scheduler.py
```

## Project status
### Implemented
- Priority queue based job scheduling
- Node filtering by CPU and memory availability
- Node scoring based on resource availability
- Data-locality bonus when `job.data_id` matches node cache
- Job binding updates node usage and job state
- Sample runner in `app/run_scheduler.py`

### Next improvements
- Add fairness and user/resource quotas
- Add job preemption and retry behavior
- Add node health checks and failure handling
- Add richer affinity/taint support
- Add logging for scheduler decisions, job assignment, and node state changes
- Add retry/backoff for transient scheduler and node failures
- Add crash tracking and alerting for runtime exceptions
- Add multithreading or async job dispatching to support concurrent scheduling
- Add automated tests for scheduler logic, node filtering, and binding
- Add monitoring and observability for job state, node utilization, and scheduling failures
- Expose scheduling operations through a simple API endpoint for remote submission and status queries



