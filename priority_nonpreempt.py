# !! PRIORITY NON-PREEMPTIVE !! 

class Process:
    def __init__(self, process_num, arrival_time, burst_time, priority_num):
        self.process_num = process_num
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority_num = priority_num
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
    priority_num = int(input(f"Enter priority number for process {process_num}: "))
    return Process(process_num, arrival_time, burst_time, priority_num)       
            
def display_table(processes):
    #make the table display processes in order of process number/id
    processes = sorted(processes, key=lambda p: p.process_num)
    print()
    print("Table for processes:")
    print("{:<15} {:<14} {:<14} {:<11} {:<17} {:<17} {:<12}".format(
        "Process Number", "Arrival Time", "Priority", "Burst Time", "Completion Time", "Turnaround Time", "Waiting Time"))
    for p in processes:
        print("P{:<14} {:<14} {:<14} {:<11} {:<17} {:<17} {:<12}".format(
            p.process_num, p.arrival_time, p.priority_num, p.burst_time, p.completion_time, p.turnaround_time, p.waiting_time))
    print()
        
#sort processes based on priority non-preemptive algo
def prioritynp_algo(processes):
    new = []
    current_time = 0
    while processes:
        temp = [p for p in processes if p.arrival_time <= current_time]  
        if temp:
            higher_prio = min(temp, key=lambda p:p.priority_num)
            new.append(higher_prio)
            processes.remove(higher_prio)
            current_time += higher_prio.burst_time
        else:
            current_time += 1     
              
    return new
        
def make_ganttchart(processes):
    current_time = 0
    ganttchart = []
    for p in processes:
        if p.arrival_time > current_time:
            ganttchart.append(("idle", current_time, p.arrival_time))
            current_time = p.arrival_time
        ganttchart.append((f"P{p.process_num}", current_time, current_time + p.burst_time))
        current_time += p.burst_time
        
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
print("Priority Non-Preemptive CPU Scheduling Algorithm:")
print()

#use this if you want to input the process details yourself
num_of_processes = int(input("Enter the number of processes included: "))
processes = []
for x in range(1, num_of_processes + 1):
    processes.append(input_process(x))

'''
#testing algo without input
processes = [
        Process(1, 3, 4, 2),
        Process(2, 5, 9, 1),
        Process(3, 8, 4, 2),
        Process(4, 0, 7, 1),
        Process(5, 12, 6, 1)
    ]
num_of_processes = 5
'''

print()
print("Priority Non-Preemptive CPU Scheduling Algorithm:")
print()
    
#rearrangement of process based on algo // SJF
processes = prioritynp_algo(processes)
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

