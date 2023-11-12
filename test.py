from prettytable import PrettyTable

class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.queue = 1
        self.resptime = -1
        self.completion_time = 0
        self.endtime = 0  # Initialize endtime to 0
        self.waiting_time = 0  # Initialize waiting time to 0

def scheduling(dataset, Q1, Q2):
    time = 0
    proc = dataset
    R2 = []
    R3 = []
    FCFS = []
    compprocesses = []
    FirstGANTT = []
    SecondGANTT = []
    ThirdGANTT = []

    while len(compprocesses) < len(proc):
        for process in proc:
            if process.arrival_time <= time and process.queue == 1 and process not in R2 and process not in compprocesses:
                R2.append(process)
                FirstGANTT.append((process.name, time))

        if len(R2) > 0:
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

            if len(R3) > 0:
                k = R3.pop(0)
                if k.resptime == -1:
                    k.resptime = time - k.arrival_time
                if k.remaining_time > Q2:
                    k.remaining_time -= Q2
                    time += Q2
                    k.queue = Q2
                    k.waiting_time += time - k.completion_time  # Update waiting time
                    FCFS.append(k)
                else:
                    time += k.remaining_time
                    k.remaining_time = 0
                    k.completion_time = time
                    k.endtime = time
                    compprocesses.append(k)
                    SecondGANTT.append((k.name, k.endtime, k.waiting_time))
            else:
                for process in proc:
                    if process.arrival_time <= time and process.queue == 3 and process not in FCFS and process not in compprocesses:
                        FCFS.append(process)
                        ThirdGANTT.append((process.name, time))

                if len(FCFS) > 0:
                    k = FCFS.pop(0)
                    if k.resptime == -1:
                        k.resptime = time - k.arrival_time
                    time += k.remaining_time
                    k.remaining_time = 0
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

    GanttOutputs(FirstGANTT, SecondGANTT, ThirdGANTT)
    return compprocesses

def GanttOutputs(FirstGANTT, SecondGANTT, ThirdGANTT):
    print("First GANTT:")
    print("--------------")
    print(GanttChart(FirstGANTT))
    print("\nSecond GANTT:")
    print("--------------")
    print(GanttChart(SecondGANTT))
    print("\nThird GANTT:")
    print("--------------")
    print(GanttChart(ThirdGANTT))

def GanttChart(gantt_data):

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

    # Append the last process separately
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
    AVGRT = sum([data.resptime for data in dataset]) / len(dataset)
    AVGRD = sum([data.reldelay for data in dataset]) / len(dataset)

    print(f"\nAvG TAT: {AVGTAT:.1f}")
    print(f"AvG WT: {AVGWT:.1f}")
    print(f"AvG RT: {AVGRT:.1f}")
    print(f"AvG RD: {AVGRD:.1f}")

data = [
    Process(1, 3, 4),
    Process(2, 5, 9),
    Process(3, 8, 4),
    Process(4, 0, 7),
    Process(5, 12, 6)
]

#Time Slices
Q1 = 2
Q2 = 3

#CPU sched versions (WALA PANI)

result = scheduling(data, Q1, Q2)
Tableoutput(result)