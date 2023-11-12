class Process:
    def __init__(self, process_num, arrival_time, burst_time):
        self.process_num = process_num
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.completion_time = None
        self.turnaround_time = None
        self.waiting_time = None
     
    #only use when the algos are implemented (use when processes are sorted na) 
    def calculate_ct(self, previous_process):
        if previous_process is None:
            self.completion_time = self.arrival_time + self.burst_time
        else:
            self.completion_time = max(self.arrival_time, previous_process.completion_time) + self.burst_time
            
    def calculate_tt(self):
        self.turnaround_time = self.completion_time - self.arrival_time
        
    def calculate_wt(self):
        self.waiting_time = self.turnaround_time - self.burst_time        
            
def avg_wt(processes):
    sum = 0
    for p in processes:
        sum += p.waiting_time
    print(f"Average Waiting Time: {sum/num_of_processes:.2f}")

def avg_tt(processes):
    sum = 0
    for p in processes:
        sum += p.turnaround_time
    print(f"Average Turnaround Time: {sum/num_of_processes:.2f}")
    
def cpu_util(processes):
    total_bt = 0
    for p in processes:
        total_bt += p.burst_time
    cpu = (total_bt / processes[-1].completion_time) * 100
    print(f"CPU Utilization: {cpu:.2f}%")

def input_process(process_num):
    arrival_time = int(input(f"Enter arrival time for process {process_num}: "))   
    burst_time = int(input(f"Enter burst time for process {process_num}: "))
    return Process(process_num, arrival_time, burst_time)       
            
def display_table(processes):
    #make the table display processes in order of process number/id
    processes = sorted(processes, key=lambda p: p.process_num)
    print()
    print("Table for processes:")
    print("{:<15} {:<14} {:<11} {:<17} {:<17} {:<12}".format(
        "Process Number", "Arrival Time", "Burst Time", "Completion Time", "Turnaround Time", "Waiting Time"))
    for p in processes:
        print("P{:<14} {:<14} {:<11} {:<17} {:<17} {:<12}".format(
            p.process_num, p.arrival_time, p.burst_time, p.completion_time, p.turnaround_time, p.waiting_time))
    print()
        
#sort processes based on FCFS algo
def fcfs_algo(processes):
    sorted_processes = sorted(processes, key=lambda p: p.arrival_time)
    return sorted_processes
        
def make_ganttchart(processes):
    current_time = 0
    ganttchart = []
    for p in processes:
        if p.arrival_time > current_time:
            ganttchart.append(("idle", current_time, p.arrival_time))
            current_time = p.arrival_time
        ganttchart.append((f"P{p.process_num}", current_time, current_time + p.burst_time))
        current_time += p.burst_time
        
    #print the gantt chart
    print("Gantt Chart:")
    # Print the gantt chart
    print("|", end=" ")
    for i, x in enumerate(ganttchart):
        if i == 0:
            if x[1] == x[2]:
                print(f"{x[0]} ({x[1]}) |", end=" ")
            else:
                print(f"{x[0]} ({x[1]}-{x[2]}) |", end=" ")
        else:
            if x[1] == x[2]:
                print(f"{x[0]} ({x[1]}) |", end=" ")
            else:
                print(f"{x[0]} ({x[1]}-{x[2]}) |", end=" ")
    print()
        
        
        
        
print()
print("First-Come-First-Serve CPU Scheduling Algorithm")
print()

#use this if you want to input the process details yourself
num_of_processes = int(input("Enter the number of processes included: "))
processes = []

for x in range(1, num_of_processes + 1):
    processes.append(input_process(x))
    
'''
#testing algo without input
processes = [
        Process(1, 5, 5),
        Process(2, 6, 10),
        Process(3, 8, 7),
        Process(4, 1, 2),
        Process(5, 12, 6)
    ]
num_of_processes = 5
'''
print()
print("First-Come-First-Serve CPU Scheduling Algorithm")
print()
#rearrangement of process based on algo
processes = fcfs_algo(processes)   
#make gantt chart
make_ganttchart(processes)    
    
#initialize prev process for calculations   
previous_process = None
for process in processes:
    process.calculate_ct(previous_process)
    process.calculate_tt()
    process.calculate_wt()
    previous_process = process

display_table(processes)
cpu_util(processes)
avg_tt(processes)
avg_wt(processes)

