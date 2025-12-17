import sys

# Class to represent a single process (Customer in the bank)
class Process:
    def __init__(self, pid, arrival_time, burst_time, priority, queue_level):
        self.id = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.queue_level = queue_level
        
        # Tracking variables
        self.remaining_time = burst_time  # Used for Round Robin
        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0

# --- ALGORITHM 1: Round Robin (Queue 1) ---
# Each process gets a 'quantum' (4 units) of time. 
# If not done, it goes to the back of the line.
def run_round_robin(queue, current_time, quantum):
    if not queue:
        return current_time
    
    # Copy the queue list so we don't mess up the original order yet
    ready_queue = [p for p in queue]
    
    while ready_queue:
        process = ready_queue.pop(0) # Take the first person
        
        if process.remaining_time > quantum:
            # Runs for 4 units, but not finished
            current_time += quantum
            process.remaining_time -= quantum
            ready_queue.append(process) # Go back to end of line
        else:
            # Process finishes
            current_time += process.remaining_time
            process.remaining_time = 0
            process.completion_time = current_time
            
    return current_time

# --- ALGORITHM 2: Priority Scheduling (Queue 2) ---
# Highest Priority (biggest number) goes first.
def run_priority(queue, current_time):
    if not queue:
        return current_time
    
    # Sort by Priority (Descending), then by Arrival Time (Ascending)
    # The minus sign (-) on priority makes it sort largest-to-smallest
    queue.sort(key=lambda x: (-x.priority, x.arrival_time))
    
    for process in queue:
        # If CPU is idle, fast-forward to arrival time
        if current_time < process.arrival_time:
            current_time = process.arrival_time
            
        current_time += process.burst_time
        process.completion_time = current_time
        
    return current_time

# --- ALGORITHM 3: First Come First Serve (Queue 3) ---
# Simple line: Whoever arrived first runs first.
def run_fcfs(queue, current_time):
    if not queue:
        return current_time
    
    # Sort strictly by Arrival Time
    queue.sort(key=lambda x: x.arrival_time)
    
    for process in queue:
        if current_time < process.arrival_time:
            current_time = process.arrival_time
            
        current_time += process.burst_time
        process.completion_time = current_time
        
    return current_time

def main():
    print("--- Multilevel CPU Scheduler Simulation ---")
    try:
        n = int(input("Enter total number of processes: "))
    except ValueError:
        print("Please enter a valid integer.")
        return

    q1 = [] # Queue 1 (Round Robin)
    q2 = [] # Queue 2 (Priority)
    q3 = [] # Queue 3 (FCFS)
    all_processes = []

    print("Enter details: Arrival Burst Priority QueueLevel(1-3)")
    for i in range(n):
        print(f"Process P{i+1}: ", end="")
        try:
            # Read 4 numbers separated by space
            data = list(map(int, input().split()))
            
            p = Process(i+1, data[0], data[1], data[2], data[3])
            all_processes.append(p)
            
            # Sort into the correct list immediately
            if p.queue_level == 1:
                q1.append(p)
            elif p.queue_level == 2:
                q2.append(p)
            else:
                q3.append(p)
        except:
            print("Invalid input format.")
            return

    current_time = 0
    
    # 1. Run Queue 1 (Highest Priority)
    current_time = run_round_robin(q1, current_time, quantum=4)
    
    # 2. Run Queue 2 (Medium Priority)
    current_time = run_priority(q2, current_time)
    
    # 3. Run Queue 3 (Low Priority)
    current_time = run_fcfs(q3, current_time)

    # Calculate Metrics & Print Table
    total_wait = 0
    total_turnaround = 0
    
    print("\n" + "-"*75)
    print(f"{'ID':<5} | {'Queue':<5} | {'Arr':<5} | {'Burst':<5} | {'Prio':<5} | {'Comp':<5} | {'Turn':<5} | {'Wait':<5}")
    print("-"*75)

    # Sort by ID (P1, P2...) just to make the table look neat
    all_processes.sort(key=lambda x: x.id)

    for p in all_processes:
        p.turnaround_time = p.completion_time - p.arrival_time
        p.waiting_time = p.turnaround_time - p.burst_time
        
        # Handle edge case if waiting time is negative
        if p.waiting_time < 0: p.waiting_time = 0
        
        total_wait += p.waiting_time
        total_turnaround += p.turnaround_time
        
        print(f"P{p.id:<4} | {p.queue_level:<5} | {p.arrival_time:<5} | {p.burst_time:<5} | {p.priority:<5} | {p.completion_time:<5} | {p.turnaround_time:<5} | {p.waiting_time:<5}")

    print("-"*75)
    print(f"Average Turnaround Time: {total_turnaround / n:.2f}")
    print(f"Average Waiting Time:    {total_wait / n:.2f}")

if __name__ == "__main__":
    main()