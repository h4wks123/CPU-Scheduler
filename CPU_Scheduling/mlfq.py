class Process:
    def __init__(self, name, arrival_time, burst_time, position, level):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.level = level
        self.position = position
        self.completion_time = 0
        self.endtime = 0  # Initialize endtime to 0
        self.waiting_time = 0  # Initialize waiting time to 0

def FirstQuantum(data, Q1, Q2, Q3):
    
    processes = [Process(*item) for item in data]
    processes.sort(key=lambda x: x.arrival_time)
    demodataset = processes.copy()
    FirstGantt = []
    SecondGantt = []
    x = i = 0
    current_time = min(x.arrival_time for x in processes)
    
    while i < len(demodataset):
        if demodataset[i].burst_time < Q1 and demodataset[i].burst_time != 0 and demodataset[i].level == 2:
            current_time += demodataset[i].burst_time
            FirstGantt.append({'name': demodataset[i].name, 'current_time': current_time, 'end_time': demodataset[i].burst_time})
            demodataset[i].burst_time -= demodataset[i].burst_time
            demodataset[i].level -= 1
            # ADD CONDITION HERE FOR IDLE TIME
        else:
            if demodataset[i].level == 2 and demodataset[i].burst_time != 0:
                current_time += Q1
                FirstGantt.append({'name': demodataset[i].name, 'current_time': current_time, 'end_time': Q1})
                demodataset[i].burst_time -= Q1
                demodataset[i].level -= 1

                # Check if the next process exists and if its arrival_time is less than the current_time
                if i + 1 < len(demodataset) and current_time < demodataset[i + 1].arrival_time and demodataset[i].level == 1 and demodataset[i].burst_time != 0:
                    if demodataset[x].burst_time < Q2:
                        current_time += demodataset[x].burst_time
                        if (current_time < demodataset[x + 1].arrival_time and current_time != demodataset[x].burst_time):
                            current_time = demodataset[x + 1].arrival_time
                            SecondGantt.append({'name': demodataset[x].name, 'current_time': current_time, 'end_time': demodataset[x].burst_time})
                            demodataset[x].burst_time -= demodataset[x].burst_time
                            demodataset[x].level -= 1
                        else:
                            SecondGantt.append({'name': demodataset[x].name, 'current_time': current_time, 'end_time': demodataset[x].burst_time})
                            demodataset[x].burst_time -= demodataset[x].burst_time
                            demodataset[x].level -= 1                            
                    else:
                        current_time += Q2
                        if (current_time < demodataset[x + 1].arrival_time and current_time != demodataset[x].burst_time):
                            current_time = demodataset[x + 1].arrival_time
                            SecondGantt.append({'name': demodataset[x].name, 'current_time': current_time, 'end_time': Q2})
                            demodataset[x].burst_time -= Q2
                            demodataset[x].level -= 1
                        else:
                            SecondGantt.append({'name': demodataset[x].name, 'current_time': current_time, 'end_time': Q2})
                            demodataset[x].burst_time -= Q2
                            demodataset[x].level -= 1

                    x += 1

        i += 1

    SecondQuantum(demodataset, current_time, Q2, Q3, FirstGantt, SecondGantt)
     

def SecondQuantum(demodataset, current_time, Q2, Q3, FirstGantt, SecondGantt):

    i = 0
    
    while i < len(demodataset):
        if demodataset[i].burst_time < Q2 and demodataset[i].burst_time != 0 and demodataset[i].level == 1:
            current_time += demodataset[i].burst_time
            SecondGantt.append({'name': demodataset[i].name, 'current_time': current_time, 'end_time': demodataset[i].burst_time})
            demodataset[i].burst_time -= demodataset[i].burst_time
            demodataset[i].level -= 1

        else:
            if demodataset[i].level == 1 and demodataset[i].burst_time != 0:
                demodataset[i].burst_time -= Q2
                demodataset[i].level -= 1
                current_time += Q2
                SecondGantt.append({'name': demodataset[i].name, 'current_time': current_time, 'end_time': Q2})

        i += 1

    ThirdQuantum(demodataset, current_time, Q3, FirstGantt, SecondGantt)


def ThirdQuantum(demodataset, current_time, Q3, FirstGantt, SecondGantt):

    ThirdGantt = []

    if  Q3 == 1: #If Q3 is 1 then shortest job first is executed
        while True:
            min_burst_time = min((x.burst_time for x in demodataset if x.burst_time != 0), default=-1)

            if min_burst_time == -1:
                break
            else:
                i = 0
                while demodataset[i].burst_time != min_burst_time:
                    i += 1

                current_time += demodataset[i].burst_time
                ThirdGantt.append({'name': demodataset[i].name, 'current_time': current_time, 'end_time': demodataset[i].burst_time})
                demodataset[i].burst_time = 0
                demodataset[i].level -= 1

    elif Q3 == 2: #If Q3 is 2 then first come first serve is executed
        while True:
            min_arrival_time = min((x.arrival_time for x in demodataset if x.burst_time != 0), default=-1)

            if min_arrival_time == -1:
                break
            else:
                i = 0
                while demodataset[i].arrival_time != min_arrival_time: #Find index of smallest arrival time if burst time is not zero
                    i += 1

                current_time += demodataset[i].burst_time
                ThirdGantt.append({'name': demodataset[i].name, 'current_time': current_time, 'end_time': demodataset[i].burst_time})
                demodataset[i].burst_time = 0
                demodataset[i].level -= 1

    elif Q3 == 3: #If Q3 is 3 then priority non preemptive is executed
        while True:
            min_position = min((x.position for x in demodataset if x.burst_time != 0), default=-1)

            if min_position == -1:
                break
            else:
                i = 0
                while demodataset[i].position != min_position: #Find index of smallest position if burst time is not zero
                    i += 1

                current_time += demodataset[i].burst_time
                ThirdGantt.append({'name': demodataset[i].name, 'current_time': current_time, 'end_time': demodataset[i].burst_time})
                demodataset[i].burst_time = 0
                demodataset[i].level -= 1


    print("-----First Gantt Chart-----")
    FirstGanttChart(FirstGantt)
    print("-----Second Gantt Chart-----")
    RestGanttChart(SecondGantt)
    print("-----Third Gantt Chart-----")
    RestGanttChart(ThirdGantt)

    print("Gantt Chart:")
    TableOutput(FirstGantt, SecondGantt, ThirdGantt)


def FirstGanttChart(FirstGantt):
    
    if not FirstGantt:
        return "All processes have been depreciated"

    line_parts = []

    # Check if there's idle time at the beginning
    if FirstGantt[0]["current_time"] - FirstGantt[0]["end_time"] > 0:
        idle_time = FirstGantt[0]["current_time"] - FirstGantt[0]["end_time"]
        line_parts.append(f'Idle ({0} - {idle_time})')

    # Add the processes to the line
    line_parts.extend([f'P{FirstGantt[i]["name"]} ({FirstGantt[i]["current_time"] - FirstGantt[i]["end_time"]} - {FirstGantt[i]["current_time"]})' for i in range(len(FirstGantt))])

    line = " | ".join(line_parts)
    print(line)
    print("")

def RestGanttChart(RestGantt):

    if not RestGantt:
        return "All processes have been depreciated"  

    RestGantt = [process for process in RestGantt if not (process["current_time"] - process["end_time"] == process["current_time"])]
    
    line = " | ".join([f'P{RestGantt[i]["name"]} ({RestGantt[i]["current_time"] - RestGantt[i]["end_time"]} - {RestGantt[i]["current_time"]})' for i in range(len(RestGantt))])
    print(line)    
    print("")

def TableOutput(FirstGantt, SecondGantt, ThirdGantt):
    all_gantt = FirstGantt + SecondGantt + ThirdGantt

    all_gantt = [process for process in all_gantt if not (process["current_time"] - process["end_time"] == process["current_time"])]
    
    # Use a dictionary to track the highest current_time for each process
    max_current_times = {}
    for entry in all_gantt:
        process_name = entry['name']
        current_time = entry['current_time']

        if process_name not in max_current_times or current_time > max_current_times[process_name]:
            max_current_times[process_name] = current_time

    # Convert dictionary items to a list of tuples and sort by process names
    sorted_max_current_times = sorted(max_current_times.items(), key=lambda x: int(x[0]))

    processes = [Process(*item) for item in data]
    processes.sort(key=lambda x: x.name)

    # Print the results
    print("{:<15} {:<14} {:<11} {:<17} {:<17} {:<12}".format(
        "Process Number", "Arrival Time", "Burst Time", "Completion Time", "Turnaround Time", "Waiting Time"))
    i = 0
    while i < len(processes):
        print("{:<15} {:<14} {:<11} {:<17} {:<17} {:<12}".format(processes[i].name, processes[i].arrival_time,
                                                    processes[i].burst_time, sorted_max_current_times[i][1], 
                                                    sorted_max_current_times[i][1] - processes[i].arrival_time,
                                                    (sorted_max_current_times[i][1] - processes[i].arrival_time) - processes[i].burst_time))
        i += 1

    print("")
    
    # Average Turnaround Time Calculation
    avg_turnaround = sum(sorted_max_current_times[i][1] - processes[i].arrival_time for i in range(len(processes))) / len(processes)
    print(f"Average Turnaround Time: {avg_turnaround:.2f}")

    # Average Waiting Time Calculation
    avg_waiting = sum(((sorted_max_current_times[i][1] - processes[i].arrival_time) - processes[i].burst_time) for i in range(len(processes))) / len(processes)
    print(f"Average Waiting Time: {avg_waiting:.2f}")

    # Average CPU Utilization
    avg_cputil = ((max(entry[1] for entry in sorted_max_current_times) - min(data.arrival_time for data in processes)) / max(entry[1] for entry in sorted_max_current_times)) * 100
    print(f"CPU Utilization: {avg_cputil:.2f}%")


if __name__ == "__main__":

    # Q1 = 3
    # Q2 = 2
    # Q3 = 2

    # data = [
    #     (1, 5, 30, 4, 2),
    #     (2, 25, 15, 3, 2),
    #     (3, 15, 25, 1, 2),
    #     (4, 10, 10, 1, 2),
    #     (5, 20, 35, 2, 2),
    #     (6, 13, 5, 5, 2)      
    # ]

    print("Choose a CPU scheduling method for the third queue:")
    print("1 - SJF")
    print("2 - FCFS")
    print("3 - PRIORITY PREEMPTIVE")
    Q3 = int(input("Enter a value for the third time queue (1-3): "))

    if Q3 != 3:
        num_processes = int(input("Enter the number of processes: "))
        data = []

        for i in range(1, num_processes + 1):
            arrival_time = int(input(f"Enter arrival time for process {i}: "))
            burst_time = int(input(f"Enter burst time for process {i}: "))
            data.append((i, arrival_time, burst_time, 0, 2))
    else:
        num_processes = int(input("Enter the number of processes: "))
        data = []

        for i in range(1, num_processes + 1):
            arrival_time = int(input(f"Enter arrival time for process {i}: "))
            burst_time = int(input(f"Enter burst time for process {i}: "))
            priority = int(input(f"Enter priority for process {i}: "))
            data.append((i, arrival_time, burst_time, priority, 2))

    # Time Slices
    Q1 = int(input("Enter a value for the first time queue: "))
    Q2 = int(input("Enter a value for the second time queue: "))
    
    FirstQuantum(data, Q1, Q2, Q3)


    # data = [
    #     (1, 3, 4, 0, 2),
    #     (2, 5, 9, 0, 2),
    #     (3, 8, 4, 0, 2),
    #     (4, 0, 7, 0, 2),
    #     (5, 12, 6, 0, 2)    
    # ]
    # Q1 = 2
    # Q2 = 3
    # Q3 = 1

    # data = [
    #     (1, 5, 30, 4, 2),
    #     (2, 25, 15, 3, 2),
    #     (3, 15, 25, 1, 2),
    #     (4, 10, 10, 1, 2),
    #     (5, 20, 35, 2, 2),
    #     (6, 13, 5, 5, 2)        
    # ]
    # Q1 = 10
    # Q2 = 15
    # Q3 = 3

    # data = [
    #     (1, 0, 8, 0, 2),
    #     (2, 2, 4, 0, 2),
    #     (3, 4, 10, 0, 2),
    #     (4, 8, 6, 0, 2),
    #     (5, 10, 8, 0, 2)    
    #     (6, 12, 10, 0, 2)   
    # ]
    # Q1 = 2
    # Q2 = 4
    # Q3 = 1

