import sys

# Class to represent a single process
class Process:
    def __init__(self, pid, arrival_time, burst_time, priority, queue_level):
        self.id = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.queue_level = queue_level
        
        # Tracking variables
        self.remaining_time = burst_time
        self.start_time = -1  # -1 indicates not started
        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0
        self.response_time = 0

# --- ALGORITHM 1: Round Robin (Queue 1) ---
# FIXED: Now strictly checks Arrival Time
def run_round_robin(queue, current_time, quantum):
    if not queue:
        return current_time
    
    # 1. Sort initially by arrival time to respect who came first
    queue.sort(key=lambda x: x.arrival_time)
    
    # Copy queue to a local list so we don't break the main list structure
    ready_queue = [p for p in queue]
    active_queue = [] # Processes that have arrived and are ready to run
    
    while ready_queue or active_queue:
        # Move newly arrived processes into the active queue
        # We use a while loop to check multiple arrivals at the same time
        while ready_queue and ready_queue[0].arrival_time <= current_time:
            active_queue.append(ready_queue.pop(0))
            
        # If no one is here yet, but people are coming, jump time forward
        if not active_queue and ready_queue:
            current_time = ready_queue[0].arrival_time
            continue

        # If truly empty, we are done
        if not active_queue:
            break

        # Run the first process in the active queue
        process = active_queue.pop(0)
        
        # Record Start Time (First CPU touch)
        if process.start_time == -1:
            process.start_time = current_time
            
        if process.remaining_time > quantum:
            # Run for quantum, then re-queue
            current_time += quantum
            process.remaining_time -= quantum
            
            # Check for new arrivals during this time slice
            while ready_queue and ready_queue[0].arrival_time <= current_time:
                active_queue.append(ready_queue.pop(0))
            
            # Add current process back to end of line
            active_queue.append(process)
        else:
            # Finish process
            current_time += process.remaining_time
            process.remaining_time = 0
            process.completion_time = current_time
            
    return current_time

# --- ALGORITHM 2: Priority Scheduling (Queue 2) ---
def run_priority(queue, current_time):
    if not queue:
        return current_time
    
    # Sort: High Priority First (-x.priority), then Earliest Arrival
    queue.sort(key=lambda x: (-x.priority, x.arrival_time))
    
    for process in queue:
        # If CPU is idle, jump to arrival time
        if current_time < process.arrival_time:
            current_time = process.arrival_time
            
        if process.start_time == -1:
            process.start_time = current_time
            
        current_time += process.burst_time
        process.completion_time = current_time
        
    return current_time

# --- ALGORITHM 3: First Come First Serve (Queue 3) ---
def run_fcfs(queue, current_time):
    if not queue:
        return current_time
    
    # Sort: Earliest Arrival First
    queue.sort(key=lambda x: x.arrival_time)
    
    for process in queue:
        if current_time < process.arrival_time:
            current_time = process.arrival_time
            
        if process.start_time == -1:
            process.start_time = current_time
            
        current_time += process.burst_time
        process.completion_time = current_time
        
    return current_time

def main():
    print("--- Multilevel CPU Scheduler Simulation ---")
    try:
        n_input = input("Enter total number of processes: ")
        if not n_input.strip(): return 
        n = int(n_input)
    except ValueError:
        return

    q1 = [] 
    q2 = []
    q3 = []
    all_processes = []
    total_burst_time = 0

    print("Enter details: Arrival Burst Priority QueueLevel(1-3)")
    for i in range(n):
        print(f"Process P{i+1}: ", end="")
        try:
            line = input().split()
            if len(line) < 4: 
                print("Invalid input")
                continue
            data = list(map(int, line))
            
            p = Process(i+1, data[0], data[1], data[2], data[3])
            all_processes.append(p)
            total_burst_time += p.burst_time
            
            if p.queue_level == 1: q1.append(p)
            elif p.queue_level == 2: q2.append(p)
            else: q3.append(p)
        except ValueError:
            print("Invalid Input")
            return

    current_time = 0
    
    # Run Queues in Order
    current_time = run_round_robin(q1, current_time, quantum=4)
    current_time = run_priority(q2, current_time)
    current_time = run_fcfs(q3, current_time)

    # Calculate Metrics
    total_wait = 0
    total_turnaround = 0
    total_response = 0
    
    # PRINT TABLE
    print("\n" + "-"*95)
    print(f"{'ID':<4} | {'Q':<3} | {'Arr':<4} | {'Burst':<5} | {'Prio':<4} | {'Comp':<5} | {'Turn':<5} | {'Wait':<5} | {'Resp':<5}")
    print("-"*95)

    all_processes.sort(key=lambda x: x.id)

    for p in all_processes:
        p.turnaround_time = p.completion_time - p.arrival_time
        p.waiting_time = p.turnaround_time - p.burst_time
        p.response_time = p.start_time - p.arrival_time 
        
        # Sanity checks (should not be needed with fixed logic, but good for safety)
        if p.waiting_time < 0: p.waiting_time = 0
        if p.response_time < 0: p.response_time = 0
        if p.turnaround_time < 0: p.turnaround_time = 0
        
        total_wait += p.waiting_time
        total_turnaround += p.turnaround_time
        total_response += p.response_time
        
        print(f"P{p.id:<3} | {p.queue_level:<3} | {p.arrival_time:<4} | {p.burst_time:<5} | {p.priority:<4} | {p.completion_time:<5} | {p.turnaround_time:<5} | {p.waiting_time:<5} | {p.response_time:<5}")

    print("-"*95)
    
    # Final Metrics
    print(f"Avg Turnaround Time: {total_turnaround / n:.2f}")
    print(f"Avg Waiting Time:    {total_wait / n:.2f}")
    print(f"Avg Response Time:   {total_response / n:.2f}")
    
    if current_time > 0:
        throughput = n / current_time
        cpu_utilization = (total_burst_time / current_time) * 100
        print(f"Throughput:          {throughput:.4f} processes/unit time")
        print(f"CPU Utilization:     {cpu_utilization:.2f}%")

if __name__ == "__main__":
    main()