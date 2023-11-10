class Process:
    def __init__(self, process_num, arrival_time, burst_time):
        self.process_num = process_num
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0

def round_robin_scheduling(processes, time_quantum):
    n = len(processes)
    remaining_time = [process.burst_time for process in processes]
    current_time = 0
    sequence = []

    while True:
        all_processes_completed = True  # Flag to check if all processes are completed in a single time quantum

        for i in range(n):
            if processes[i].arrival_time <= current_time and remaining_time[i] > 0:
                all_processes_completed = False

                if remaining_time[i] <= time_quantum:
                    current_time += remaining_time[i]
                    sequence.append((f'P{processes[i].process_num}', current_time))
                    processes[i].completion_time = current_time
                    remaining_time[i] = 0
                else:
                    current_time += time_quantum
                    sequence.append((f'P{processes[i].process_num}', current_time))
                    remaining_time[i] -= time_quantum

        if all_processes_completed:
            # No process is ready to execute, insert idle time
            current_time += 1
            sequence.append(('idle', current_time))

        # Check if all processes are completed
        if all(time == 0 for time in remaining_time):
            break

    print("Gantt Chart:")
    i = 0

    while i < len(sequence):
        current_process = sequence[i][0]
        start_time = sequence[i][1]

        while i + 1 < len(sequence) and sequence[i][0] == sequence[i + 1][0]:
            i += 1

        end_time = sequence[i][1]

        if start_time == end_time:  # If the process only occurs at a single time point
            print(f" {current_process} ({start_time}) | ", end="")
        else:
            print(f"{current_process} ({start_time}-{end_time}) | ", end="")

        i += 1

    print()
    return sequence  # Add this line at the end

if __name__ == "__main__":
    # Test Case: 5 processes
    processes_test = [
        Process(1, 3, 4),
        Process(2, 5, 9),
        Process(3, 8, 4),
        Process(4, 0, 7),
        Process(5, 12, 6)
    ]

    time_quantum = 2
    sequence = round_robin_scheduling(processes_test, time_quantum)
