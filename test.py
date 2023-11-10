class Process:
    def __init__(self, name, arrival_time, burst_time, priority):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.remaining_time = burst_time

def priority_preemptive_scheduling(processes):
    time_chart = []
    current_time = 0

    # Sort processes based on arrival time and priority
    processes.sort(key=lambda x: (x.arrival_time, x.priority))

    while processes:
        ready_processes = [p for p in processes if p.arrival_time <= current_time]
        if not ready_processes:
            # No process is ready, add idle time to the Gantt chart
            time_chart.append((current_time, "Idle"))
            current_time += 1
            continue

        # Select the process with the highest priority
        selected_process = min(ready_processes, key=lambda x: x.priority)

        # Update the Gantt chart
        time_chart.append((current_time, selected_process.name))

        # Reduce remaining time of the selected process
        selected_process.remaining_time -= 1
        current_time += 1

        # Remove the process if it's completed
        if selected_process.remaining_time == 0:
            processes.remove(selected_process)

    return time_chart

def display_gantt_chart(time_chart): #Starts at zero
    print("Gantt Chart:")
    i = 0
    while i < len(time_chart):
        start_time, process_name = time_chart[i]

        while i + 1 < len(time_chart) and process_name == time_chart[i + 1][1]:
            i += 1        

        end_time = time_chart[i][0]

        if start_time == end_time:  # If the process only occurs at a single time point
            if start_time == 0:
                print(f" {process_name} ({0}-{1}) | ", end="")
            else:
                print(f" {process_name} ({start_time}) | ", end="")
        else:
            if start_time == 0:
                print(f"{process_name} ({start_time - 1}-{end_time}) | ", end="")
            else:
                print(f" {process_name} ({start_time}-{end_time}) | ", end="")
        i += 1

    print()

if __name__ == "__main__":
    processes = [
        Process("P1", 2, 10, 1),
        Process("P2", 13, 9, 2),
        Process("P3", 20, 7, 4),
        Process("P4", 1, 3, 5),
        Process("P5", 11, 11, 3)
    ]

    time_chart = priority_preemptive_scheduling(processes)
    display_gantt_chart(time_chart)

        # Process("P1", 3, 4, 2),
        # Process("P2", 5, 9, 1),
        # Process("P3", 8, 4, 2),
        # Process("P4", 0, 7, 1),
        # Process("P5", 12, 6, 1)