class Process:
    def __init__(self, process_num, arrival_time, burst_time):
        self.process_num = process_num
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0

def input_process(process_num):
    arrival_time = int(input(f"Enter arrival time for process {process_num}: "))   
    burst_time = int(input(f"Enter burst time for process {process_num}: "))
    return Process(process_num, arrival_time, burst_time)

def avg_wt(processes):
    sum_wt = 0
    for p in processes:
        sum_wt += p.waiting_time
    return sum_wt / len(processes)

def avg_tt(processes):
    sum_tt = 0
    for p in processes:
        sum_tt += p.turnaround_time
    return sum_tt / len(processes)

def cpu_util(sequence):
    total_idle_time = sum(1 for process, _ in sequence if process == 'idle')
    total_time = sequence[-1][1]  # Assuming the last entry in the sequence is the completion time
    utilization = ((total_time - total_idle_time) / total_time) * 100
    print(f"CPU Utilization: {utilization:.2f}%")

def display_table(processes):
    print()
    print("Table for processes:")
    print("{:<15} {:<14} {:<11} {:<17} {:<17} {:<12}".format(
        "Process Number", "Arrival Time", "Burst Time", "Completion Time", "Turnaround Time", "Waiting Time"))
    for p in processes:
        print("P{:<14} {:<14} {:<11} {:<17} {:<17} {:<12}".format(
            p.process_num, p.arrival_time, p.burst_time, p.completion_time, p.turnaround_time, p.waiting_time))
    print()

def srtf_scheduling(processes):
    n = len(processes)
    remaining_time = [process.burst_time for process in processes]
    completion_time = [0] * n
    current_time = 0
    sequence = []

    while True:
        shortest_job_index = -1
        shortest_job_time = float('inf')

        for i in range(n):
            if processes[i].arrival_time <= current_time and remaining_time[i] < shortest_job_time and remaining_time[i] > 0:
                shortest_job_index = i
                shortest_job_time = remaining_time[i]

        if shortest_job_index == -1:
            # No process is ready to execute, insert idle time
            current_time += 1
            sequence.append(('idle', current_time))
        else:
            remaining_time[shortest_job_index] -= 1
            current_time += 1

            completion_time[shortest_job_index] = current_time
            sequence.append((f'P{processes[shortest_job_index].process_num}', current_time))

            if remaining_time[shortest_job_index] == 0:
                processes[shortest_job_index].completion_time = current_time
                processes[shortest_job_index].turnaround_time = current_time - processes[shortest_job_index].arrival_time
                processes[shortest_job_index].waiting_time = processes[shortest_job_index].turnaround_time - processes[shortest_job_index].burst_time

        # Check if all processes are completed
        if all(time == 0 for time in remaining_time):
            break
    
    
    print("Gantt Chart:")
    i = 0

    while i < len(sequence): #Stored value starts at one
        current_process = sequence[i][0]
        start_time = sequence[i][1]

        while i + 1 < len(sequence) and sequence[i][0] == sequence[i + 1][0]:
            i += 1

        end_time = sequence[i][1]

        if start_time == end_time:  # If the process only occurs at a single time point
            if start_time == 1:
                print(f" {current_process} ({0}-{1}) | ", end="")
            else:
                print(f" {current_process} ({start_time}) | ", end="")
        else:
            if start_time == 1:
                print(f"{current_process} ({start_time - 1}-{end_time}) | ", end="")
            else:
                print(f" {current_process} ({start_time}-{end_time}) | ", end="")
        i += 1

    print()
    return sequence  # Add this line at the end of the function


if __name__ == "__main__":
    # Test Case: 5 processes
    processes_test = [
        Process(1, 4, 5),
        Process(2, 8, 10),
        Process(3, 3, 7),
        Process(4, 6, 8),
        Process(5, 0, 6)
    ]

    sequence = srtf_scheduling(processes_test)

    display_table(processes_test)
    cpu_util(sequence)

    print(f"Average Turnaround Time: {avg_tt(processes_test):.2f}")
    print(f"Average Waiting Time: {avg_wt(processes_test):.2f}")

        # Second Test Case
        # Process(1, 3, 4),
        # Process(2, 5, 9),
        # Process(3, 8, 4),
        # Process(4, 0, 7),
        # Process(5, 12, 6)

        # Third Test Case
        # Process(1, 3, 4),
        # Process(2, 9, 5),
        # Process(3, 10, 9),
        # Process(4, 8, 12),
        # Process(5, 12, 10)