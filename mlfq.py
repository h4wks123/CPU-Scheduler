from prettytable import PrettyTable

class Process:
    def __init__(self, name, arrival_time, burst_time, position):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.position = position
        self.queue = 1
        self.resptime = -1
        self.completion_time = 0
        self.endtime = 0  # Initialize endtime to 0
        self.waiting_time = 0  # Initialize waiting time to 0

def scheduling(dataset, Q1, Q2, Q3):
    time = 0
    proc = dataset
    R2 = []
    R3 = []
    R4 = []
    compprocesses = []
    FirstGANTT = []
    SecondGANTT = []
    ThirdGANTT = []

    while len(compprocesses) < len(proc):
        for process in proc:
            if process.arrival_time <= time and process.queue == 1 and process not in R2 and process not in compprocesses:
                R2.append(process)
                FirstGANTT.append((process.name, time))

        if len(R2) > 0: #First time quantum
            k = R2.pop(0)
            if k.resptime == -1:
                k.resptime = time - k.arrival_time
            if k.remaining_time > Q1:
                k.remaining_time -= Q1
                time += Q1
                k.queue = Q1
                k.waiting_time += time - k.completion_time  # Update waiting time
                R3.append(k)
            else:
                time += k.remaining_time
                k.remaining_time = 0
                k.completion_time = time
                k.endtime = time
                compprocesses.append(k)
                FirstGANTT.append((k.name, k.endtime, k.waiting_time))
        else:
            for process in proc:
                if process.arrival_time <= time and process.queue == 2 and process not in R3 and process not in compprocesses:
                    R3.append(process)
                    SecondGANTT.append((process.name, time))

            if len(R3) > 0: #Second time quantum
                k = R3.pop(0)
                if k.resptime == -1:
                    k.resptime = time - k.arrival_time
                if k.remaining_time > Q2:
                    k.remaining_time -= Q2
                    time += Q2
                    k.queue = Q2
                    k.waiting_time += time - k.completion_time  # Update waiting time
                    R4.append(k)
                else:
                    time += k.remaining_time
                    k.remaining_time = 0
                    k.completion_time = time
                    k.endtime = time
                    compprocesses.append(k)
                    SecondGANTT.append((k.name, k.endtime, k.waiting_time))
            else:
                for process in proc:
                    if process.arrival_time <= time and process.queue == 3 and process not in R4 and process not in compprocesses:
                        R4.append(process)
                        ThirdGANTT.append((process.name, time))

                if Q3 == 1 and len(R4) > 0: #FCFS Process aron ma sort ang last queue
                    k = R4.pop(0)
                    if k.resptime == -1:
                        k.resptime = time - k.arrival_time
                    time += k.remaining_time
                    k.remaining_time = 0
                    k.completion_time = time
                    k.endtime = time
                    compprocesses.append(k)
                    ThirdGANTT.append((k.name, k.endtime, k.waiting_time))
                elif Q3 == 2 and len(R4) > 0:
                    R4.sort(key=lambda x: x.remaining_time)  # SJF, Sort using burst time ambot gikapoy nakoooo
                    k = R4.pop(0)
                    if k.resptime == -1:
                        k.resptime = time - k.arrival_time
                    time += k.remaining_time
                    k.remaining_time = 0
                    k.completion_time = time
                    k.endtime = time
                    compprocesses.append(k)
                    ThirdGANTT.append((k.name, k.endtime, k.waiting_time))
                elif Q3 == 3 and len(R4) > 0:
                    # Priority Preemption: Sort by priority, lower values mean higher priority
                    R4.sort(key=lambda x: x.position)  
                    k = R4.pop(0)
                    if k.resptime == -1:
                        k.resptime = time - k.arrival_time
                    time += 1  # Time quantum for priority preemptive
                    k.remaining_time -= 1
                    k.completion_time = time
                    k.endtime = time
                    compprocesses.append(k)
                    ThirdGANTT.append((k.name, k.endtime, k.waiting_time))
                else:
                    time += 1

    for process in compprocesses:
        process.turnaround = process.completion_time - process.arrival_time
        process.waittime = process.turnaround - process.burst_time
        process.reldelay = round(process.waittime / process.burst_time, 2)

    GanttOutputs(FirstGANTT, SecondGANTT, ThirdGANTT, Q1, Q2)
    return compprocesses

def GanttOutputs(FirstGANTT, SecondGANTT, ThirdGANTT, Q1, Q2):
    print("First GANTT:")
    print("--------------")
    print(GanttChart(FirstGANTT, Q1))
    print("\nSecond GANTT:")
    print("--------------")
    print(GanttChart(SecondGANTT, Q2))
    print("\nThird GANTT:")
    print("--------------")
    print(ThirdGanttChart(ThirdGANTT))

def GanttChart(gantt_data, time_queue_slice): #Sorting first and second queue based on time slice

    if not gantt_data:
        return "All processes have been depreciated"

    min_arrival_time = gantt_data[0][1]
    start_index = min_arrival_time
    result = []

    for i in range(len(gantt_data) - 1):
        if start_index == gantt_data[i + 1][1]:
            result.append(f'P{gantt_data[i][0]} ({start_index})')
            start_index = gantt_data[i + 1][1] + 1
        else:
            result.append(f'P{gantt_data[i][0]} ({start_index} - {start_index + time_queue_slice})')
            start_index = gantt_data[i + 1][1]

    if start_index == gantt_data[-1][1]:
        result.append(f'P{gantt_data[-1][0]} ({start_index})')
    else:
        result.append(f'P{gantt_data[-1][0]} ({start_index} - {start_index + time_queue_slice})')

    return " | ".join(result)

def ThirdGanttChart(gantt_data):
    if not gantt_data:
        return "All processes have been depreciated"

    min_arrival_time = gantt_data[0][1]
    start_index = min_arrival_time
    result = []

    for i in range(len(gantt_data) - 1):
        if start_index == gantt_data[i + 1][1]:
            result.append(f'P{gantt_data[i][0]} ({start_index})')
            start_index = gantt_data[i + 1][1] + 1
        else:
            result.append(f'P{gantt_data[i][0]} ({start_index} - {gantt_data[i + 1][1] - 1})')
            start_index = gantt_data[i + 1][1]

    if start_index == gantt_data[-1][1]:
        result.append(f'P{gantt_data[-1][0]} ({start_index})')
    else:
        result.append(f'P{gantt_data[-1][0]} ({start_index} - {gantt_data[-1][1]})')

    return " | ".join(result)


def Tableoutput(dataset):
    Ta = PrettyTable()
    Ta.field_names = ["Process ID", "Arrival Time", "Burst Time", "Completion Time", "Turnaround Time", "Waiting Time"]
    dataset.sort(key=lambda x: x.name)
    for row in dataset:
        Ta.add_row([row.name, row.arrival_time, row.burst_time, row.endtime, row.turnaround, row.waiting_time])
    print(Ta)

    AVGTAT = sum([data.turnaround for data in dataset]) / len(dataset)
    AVGWT = sum([data.waittime for data in dataset]) / len(dataset)
    cpu_utilization = ((max(data.endtime for data in dataset)) - min(data.arrival_time for data in dataset)) / (max(data.endtime for data in dataset)) * 100

    print(f"\nAverage Turnaround Time: {AVGTAT:.1f}")
    print(f"Average Waiting Time: {AVGWT:.1f}")
    print(f"CPU Utilization: {cpu_utilization:.1f}%")  

if __name__ == "__main__":


    #CPU sched versions
    print("Choose a CPU scheduling method for the third queue:")
    print("1 - FCFS")
    print("2 - SJF")
    print("3 - PRIORITY PREEMPTIVE")
    Q3 = int(input("Enter a value for the third time queue (1-3): "))

    if Q3 != 3:
        num_processes = int(input("Enter the number of processes: "))
        data = []

        for i in range(1, num_processes + 1):
            arrival_time = int(input(f"Enter arrival time for process {i}: "))
            burst_time = int(input(f"Enter burst time for process {i}: "))
            data.append(Process(i, arrival_time, burst_time, 0))
    else:
        num_processes = int(input("Enter the number of processes: "))
        data = []

        for i in range(1, num_processes + 1):
            arrival_time = int(input(f"Enter arrival time for process {i}: "))
            burst_time = int(input(f"Enter burst time for process {i}: "))
            priority = int(input(f"Enter priority for process {i}: "))
            data.append(Process(i, arrival_time, burst_time, priority))

        #Time Slices
    Q1 = int(input("Enter a value for the first time queue: "))
    Q2 = int(input("Enter a value for the second time queue: "))

    result = scheduling(data, Q1, Q2, Q3)
    Tableoutput(result)


# Test Case 1

# Process(1, 3, 4, 3),
# Process(2, 5, 9, 2),
# Process(3, 8, 4, 1),
# Process(4, 0, 7, 4),
# Process(5, 12, 6, 5)
# First Time Quantum 2
# Second Time Quantum 3


