class Process:
    def __init__(self, name, arrival_time, burst_time, priority):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.remaining_time = burst_time
        self.completion_time = 0
        self.turnaround_time = 0  
        self.waiting_time = 0 

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
    total_idle_time = sum(1 for _, process in sequence if process == 'idle')
    total_time = sequence[-1][0] + 1  # Assuming the last entry in the sequence is the completion time
    utilization = ((total_time - total_idle_time) / total_time) * 100
    print(f"CPU Utilization: {utilization:.2f}%")

    
def display_table_with_results(processes):
    # Sort processes based on their original order (by name)
    processes.sort(key=lambda x: x.name)

    print()
    print("Table for processes:")
    print("{:<15} {:<14} {:<11} {:<11} {:<17} {:<17} {:<12}".format(
        "Process Number", "Arrival Time", "Burst Time", "Priority Level", "Completion Time", "Turnaround Time", "Waiting Time"))
    for p in processes:
        print("{:<15} {:<14} {:<11} {:<17} {:<17} {:<17} {:<12}".format(
            p.name, p.arrival_time, p.burst_time, p.priority, p.completion_time, p.turnaround_time, p.waiting_time))
    print()



def priority_preemptive_scheduling_with_gantt(processes):
    time_chart = []
    current_time = 0

    # Sort processes based on arrival time and priority
    processes.sort(key=lambda x: (x.arrival_time, x.priority))

    # Create a copy of the processes list to store the results
    result_processes = processes.copy()

    while processes:
        ready_processes = [p for p in processes if p.arrival_time <= current_time]
        if not ready_processes:
            # No process is ready, add idle time to the Gantt chart
            time_chart.append((current_time, "idle"))
            current_time += 1
            continue

        # Select the process with the highest priority
        selected_process = min(ready_processes, key=lambda x: x.priority)

        # Update the Gantt chart
        time_chart.append((current_time, f'P{selected_process.name}'))

        # Reduce remaining time of the selected process
        selected_process.remaining_time -= 1
        current_time += 1

        # Check if the process is completed
        if selected_process.remaining_time == 0:
            # Update completion time, turnaround time, and waiting time
            selected_process.completion_time = current_time
            selected_process.turnaround_time = current_time - selected_process.arrival_time
            selected_process.waiting_time = selected_process.turnaround_time - selected_process.burst_time

        # Remove the process if it's completed
        if selected_process.remaining_time == 0:
            processes.remove(selected_process)

    # Display Gantt Chart
    print("Gantt Chart:")
    i = 0
    while i < len(time_chart):
        start_time, process_name = time_chart[i]

        while i + 1 < len(time_chart) and process_name == time_chart[i + 1][1]:
            i += 1        

        end_time = time_chart[i][0]

        if start_time == end_time:  # If the process only occurs at a single time point
            if start_time == 0:
                print(f" {process_name} ({0} - {1}) | ", end="")
            else:
                print(f" {process_name} ({start_time} - {end_time + 1}) | ", end="")
        else:
            if start_time == 0:
                print(f"{process_name} ({0} - {end_time + 1}) | ", end="")
            else:
                print(f" {process_name} ({start_time} - {end_time + 1}) | ", end="")
        i += 1

    print()
    
    # Display the table using the copied list with results
    display_table_with_results(result_processes)

    print(f"Average Turnaround Time: {avg_tt(result_processes):.2f}")
    print(f"Average Waiting Time: {avg_wt(result_processes):.2f}")

    return time_chart

if __name__ == "__main__":
    processes = [
        Process(1, 1, 5, 3),
        Process(2, 3, 7, 2),
        Process(3, 6, 3, 1),
        Process(4, 9, 8, 4),
        Process(5, 11, 6, 5)
    ]

    sequence = priority_preemptive_scheduling_with_gantt(processes)
    cpu_util(sequence)










        # First Test Case
        # Process(1, 2, 10, 1),
        # Process(2, 13, 9, 2),
        # Process(3, 20, 7, 4),
        # Process(4, 1, 3, 5),
        # Process(5, 11, 11, 3)

        # Second Test Case
        # Process(1, 3, 4, 2),
        # Process(2, 5, 9, 1),
        # Process(3, 8, 4, 2),
        # Process(4, 0, 7, 1),
        # Process(5, 12, 6, 1)

        # Third Test Case
        # Process(1, 1, 5, 3),
        # Process(2, 3, 7, 2),
        # Process(3, 6, 3, 1),
        # Process(4, 9, 8, 4),
        # Process(5, 11, 6, 5)

        # Fourth Test Case
        # Process(1, 0, 6, 2),
        # Process(2, 2, 8, 1),
        # Process(3, 4, 5, 3),
        # Process(4, 7, 7, 4),
        # Process(5, 10, 9, 2)

        # Fifth Test Case
        # Process(1, 9, 10, 1),
        # Process(2, 13, 9, 2),
        # Process(3, 10, 7, 4),
        # Process(4, 3, 3, 5),
        # Process(5, 11, 11, 3)