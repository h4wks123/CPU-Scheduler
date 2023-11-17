# !! MULTILEVEL QUEUE ALGORITHM !! 
import copy

class Process:
    def __init__(self, process_num, arrival_time, burst_time, priority_num, queue_level):
        self.process_num = process_num
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority_num = priority_num
        self.queue_level = queue_level
        self.completion_time = None
        self.turnaround_time = None
        self.waiting_time = None
        self.remaining_time = burst_time
     
    def __str__(self):
        return f"Process {self.process_num} - Arrival Time: {self.arrival_time}, Burst Time: {self.burst_time}, Priority: {self.priority_num}, Queue Level: {self.queue_level}"
    
    #only use when the algos are implemented (use when processes are sorted na) 
    def calculate_ct(self, previous_process):
        if previous_process is None:
            self.completion_time = self.arrival_time + self.burst_time
        else:
            self.completion_time = max(self.arrival_time, previous_process.completion_time + 1) + self.burst_time
            
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
    max_completion_time_process = max(processes, key=lambda process: process.completion_time)
    cpu = (total_bt / max_completion_time_process.completion_time) * 100
    print(f"CPU Utilization: {cpu:.2f}%")

def input_process(process_num):
    arrival_time = int(input(f"Enter arrival time for process {process_num}: "))   
    burst_time = int(input(f"Enter burst time for process {process_num}: "))
    print("Note: If no priority number needed, just input 1")
    priority_num = int(input(f"Enter priority number for process {process_num}: "))
    queue_level = int(input(f"Enter queue level for process {process_num}: "))
    return Process(process_num, arrival_time, burst_time, priority_num, queue_level)       
            
def display_table(processes):
    #make the table display processes in order of process number/id
    processes = sorted(processes, key=lambda p: p.process_num)
    print()
    print("Table for processes:")
    print("{:<15} {:<14} {:<14} {:<11} {:<14} {:<17} {:<17} {:<12}".format(
        "Process Number", "Arrival Time", "Burst Time", "Priority", "Queue Level", "Completion Time", "Turnaround Time", "Waiting Time"))
    for p in processes:
        p.calculate_tt()
        p.calculate_wt()
        print("P{:<14} {:<14} {:<14} {:<11} {:<14} {:<17} {:<17} {:<12}".format(
            p.process_num, p.arrival_time, p.burst_time, p.priority_num, p.queue_level, p.completion_time, p.turnaround_time, p.waiting_time))
    print()

def next_arrived_time(processes, current_time):
    next_arrival = float('inf')
    for p in processes:
        if p.arrival_time > current_time and p.arrival_time < next_arrival:
            next_arrival = p.arrival_time
    return next_arrival if next_arrival != float('inf') else None

def get_smallest_id(processes):
    smallest_id_process = min(processes, key=lambda p: p.process_num)
    return smallest_id_process

#algos involved will be placed here
#all algos should return a process, not a list of processes now

#sort processes based on FCFS algo
def fcfs_algo(processes):
    sorted_processes = sorted(processes, key=lambda p: p.arrival_time)
    first_process = sorted_processes[0]
    return first_process

#sort processes based on SJF algo
def sjf_algo(processes):
    sorted_processes = sorted(processes, key=lambda p: p.burst_time)
    
    if len(sorted_processes) > 1:
        if sorted_processes[0].burst_time == sorted_processes[1].burst_time:
            shortest_process = fcfs_algo(sorted_processes)
        else:
            shortest_process = sorted_processes[0]
    else: 
        shortest_process = sorted_processes[0]
    '''
    shortest_process = sorted_processes[0]
    '''
    return shortest_process
      
#sort processes based on priority non-preemptive algo
#if more than one process has the same priority, change to find shortest burst, or earliest process
def prioritynp_algo(processes):
    if not processes:
        return None  # Return None if the input list is empty

    sorted_processes = sorted(processes, key=lambda p: p.priority_num)
    num_highestprio = 0
    highestprio_index = sorted_processes[0].priority_num
    for p in sorted_processes:
        if p.priority_num == highestprio_index:
            num_highestprio += 1
    if num_highestprio > 1:
        sorted_processes = [p for p in processes if p.priority_num == highestprio_index]
        highest_priority = sjf_algo(sorted_processes)  #use sjf algo
    elif num_highestprio == 1:
        highest_priority = sorted_processes[0]
    return highest_priority
 
#attempt at mlq algo
def mlq_algo(processes, top_queue, bottom_queue, time_quantum):
    current_time = 0
    copy_list = processes[:] #copy list to be popped every instance a process is executed
    sequence_list = [] #list used to show sequence in gantt
    queued_list = [] #for round robin queue
    
    #while the copy list is not empty
    while copy_list:
        eligible_processes = [p for p in copy_list if p.arrival_time <= current_time]
        
        #if there are no eligible processes
        if not eligible_processes:
            # Check if sequence_list is not empty before accessing the last element
            if sequence_list and sequence_list[-1][0] == "idle":
                # Convert the last element to a list so that it can be modified
                last_element_list = list(sequence_list[-1])
                last_element_list[2] = current_time + 1
                sequence_list[-1] = tuple(last_element_list)
            else:
                sequence_list.append(("idle", current_time, current_time))
            current_time += 1


        #if there are eligible processes
        elif len(eligible_processes) >= 1:
            #get processes with higher queue level
            higher_queue = [q for q in eligible_processes if q.queue_level == 1]
            
            #if higher queue has processes
            if higher_queue:
                #perform algo based on queue level algo
                if top_queue == 1 or top_queue == 2 or top_queue == 3:
                    if top_queue == 1:
                        process = fcfs_algo(higher_queue)
                    elif top_queue == 2:
                        process = sjf_algo(higher_queue)
                    elif top_queue == 3:
                        process = prioritynp_algo(higher_queue)
                    start_time = current_time
                    end_time = current_time + process.burst_time
                    completion_time = end_time
                    sequence_list.append((process.process_num, start_time, end_time))
                        
                    # Append completion time to the original processes list
                    index = [i for i, p in enumerate(processes) if p.process_num == process.process_num][0]
                    processes[index].completion_time = completion_time

                    copy_list.remove(process)
                    current_time = end_time
                    
                elif top_queue == 4 or top_queue == 5:  #srtf or prio
                    #get next arrival time
                    next_at = next_arrived_time(copy_list, current_time)
                    
                    if top_queue == 4:
                        process = sjf_algo(higher_queue) #get process with shortest burst
                    elif top_queue == 5:
                        process = prioritynp_algo(higher_queue) #get process with highest prio
                    
                    if next_at == None or next_at >= process.burst_time+current_time:
                        start_time = current_time
                        end_time = current_time + process.burst_time
                        completion_time = end_time
                        sequence_list.append((process.process_num, start_time, end_time))
                        
                        # Append completion time to the original processes list
                        index = [i for i, p in enumerate(processes) if p.process_num == process.process_num][0]
                        processes[index].completion_time = completion_time
                        
                        copy_list.remove(process)
                        current_time = end_time
                        
                    elif next_at <= process.burst_time + current_time:
                        #calculate remaining time, replace copy list index burst with remaining time
                        executed_time = next_at - current_time
                        remaining_time = process.burst_time - executed_time
                        
                        #set start and end time
                        start_time = current_time
                        end_time = current_time + executed_time
                        completion_time = end_time
                        
                        #append remaining time to copy list
                        index = [i for i, p in enumerate(copy_list) if p.process_num == process.process_num][0]
                        copy_list[index] = copy.copy(copy_list[index])
                        copy_list[index].burst_time = remaining_time

                        
                        #append completion time to original list
                        index = [i for i, p in enumerate(processes) if p.process_num == process.process_num][0]
                        processes[index].completion_time = completion_time
                        
                        
                        # Check if sequence_list is not empty before accessing the last element
                        #check if last element process num is same as current process num
                        if sequence_list and sequence_list[-1][0] == process.process_num:
                            # Convert the last element to a list so that it can be modified
                            last_element_list = list(sequence_list[-1])
                            last_element_list[2] = current_time + executed_time
                            sequence_list[-1] = tuple(last_element_list)
                        else:
                            #append new process executed to sequence
                            sequence_list.append((process.process_num, start_time, end_time))
                        
                        current_time += executed_time
                 
                #round robin hehe   
                elif top_queue == 6:
                    #if there are processes in queue
                    if queued_list:
                        if all(elem in queued_list for elem in higher_queue):
                            # If yes, make eligible_list a copy of queue_list
                            higher_queue = queued_list.copy()
                        else:
                            # If not, remove common elements in eligible_list, leaving only uncommon elements
                            common_elements = set(higher_queue) & set(queued_list)
                            higher_queue = [elem for elem in higher_queue if elem not in common_elements]
                            

                    #get process to be executed
                    if len(higher_queue) == 1:
                        process = higher_queue[0]
                    elif len(higher_queue) > 1 and higher_queue != queued_list:
                        process = fcfs_algo(higher_queue)
                    elif len(higher_queue) > 1 and higher_queue == queued_list:
                        process = higher_queue[0]
                        
                    #determines if process stays in queue, joins queue, or exits queue
                    if process.remaining_time > time_quantum:
                        end_time = current_time + time_quantum
                        process.remaining_time -= time_quantum
                        
                        #only append process if it doesnt exist already
                        if process in queued_list:
                            queued_list.remove(process)
                        
                        queued_list.append(process)
                        
                    elif process.remaining_time <= time_quantum:
                        end_time = current_time + process.remaining_time
                        process.remaining_time = 0
                            
                        #append completion time to original list
                        index = [i for i, p in enumerate(processes) if p.process_num == process.process_num][0]
                        processes[index].completion_time = end_time
                            
                        copy_list.remove(process)
                        if process in queued_list:
                            queued_list.remove(process)
                        

                    #append to sequence list
                    start_time = current_time
                    sequence_list.append((process.process_num, start_time, end_time))
                    current_time = end_time
                             
                                    
            #if there is not higher_queue
            else: 
                #perform algo based on queue level algo
                if bottom_queue == 1 or bottom_queue == 2 or bottom_queue == 3:
                    if bottom_queue == 1:
                        process = fcfs_algo(eligible_processes)
                    elif bottom_queue == 2:
                        process = sjf_algo(eligible_processes)
                    elif bottom_queue == 3:
                        process = prioritynp_algo(eligible_processes)
                    start_time = current_time
                    end_time = current_time + process.burst_time
                    completion_time = end_time
                    sequence_list.append((process.process_num, start_time, end_time))
                        
                    # Append completion time to the original processes list
                    index = [i for i, p in enumerate(processes) if p.process_num == process.process_num][0]
                    processes[index].completion_time = completion_time

                    copy_list.remove(process)
                    current_time = end_time
                    
                elif bottom_queue == 4 or bottom_queue == 5:  #srtf or prio
                    #get next arrival time
                    next_at = next_arrived_time(copy_list, current_time)
                    
                    if bottom_queue == 4:
                        process = sjf_algo(eligible_processes) #get process with shortest burst
                    elif bottom_queue == 5:
                        process = prioritynp_algo(eligible_processes) #get process with highest prio
                    
                    if next_at == None or next_at >= process.burst_time+current_time:
                        start_time = current_time
                        end_time = current_time + process.burst_time
                        completion_time = end_time
                        sequence_list.append((process.process_num, start_time, end_time))
                        
                        # Append completion time to the original processes list
                        index = [i for i, p in enumerate(processes) if p.process_num == process.process_num][0]
                        processes[index].completion_time = completion_time
                        
                        copy_list.remove(process)
                        current_time = end_time
                        
                    elif next_at <= process.burst_time + current_time:
                        #calculate remaining time, replace copy list index burst with remaining time
                        executed_time = next_at - current_time
                        remaining_time = process.burst_time - executed_time
                        
                        #set start and end time
                        start_time = current_time
                        end_time = current_time + executed_time
                        completion_time = end_time
                        
                        #append remaining time to copy list
                        index = [i for i, p in enumerate(copy_list) if p.process_num == process.process_num][0]
                        copy_list[index] = copy.copy(copy_list[index])
                        copy_list[index].burst_time = remaining_time

                        
                        #append completion time to original list
                        index = [i for i, p in enumerate(processes) if p.process_num == process.process_num][0]
                        processes[index].completion_time = completion_time
                        
                        
                        # Check if sequence_list is not empty before accessing the last element
                        #check if last element process num is same as current process num
                        if sequence_list and sequence_list[-1][0] == process.process_num:
                            # Convert the last element to a list so that it can be modified
                            last_element_list = list(sequence_list[-1])
                            last_element_list[2] = current_time + executed_time
                            sequence_list[-1] = tuple(last_element_list)
                        else:
                            #append new process executed to sequence
                            sequence_list.append((process.process_num, start_time, end_time))
                        
                        current_time += executed_time
                 
                #round robin hehe   
                elif bottom_queue == 6:
                    #if there are processes in queue
                    if queued_list:
                        if all(elem in queued_list for elem in eligible_processes):
                            # If yes, make eligible_list a copy of queue_list
                            eligible_processes = queued_list.copy()
                        else:
                            # If not, remove common elements in eligible_list, leaving only uncommon elements
                            common_elements = set(eligible_processes) & set(queued_list)
                            eligible_processes = [elem for elem in eligible_processes if elem not in common_elements]
                            

                    #get process to be executed
                    if len(eligible_processes) == 1:
                        process = eligible_processes[0]
                    elif len(eligible_processes) > 1 and eligible_processes != queued_list:
                        process = fcfs_algo(eligible_processes)
                    elif len(eligible_processes) > 1 and eligible_processes == queued_list:
                        process = eligible_processes[0]
                        
                    #determines if process stays in queue, joins queue, or exits queue
                    if process.remaining_time > time_quantum:
                        end_time = current_time + time_quantum
                        process.remaining_time -= time_quantum
                        
                        #only append process if it doesnt exist already
                        if process in queued_list:
                            queued_list.remove(process)
                        
                        queued_list.append(process)
                        
                    elif process.remaining_time <= time_quantum:
                        end_time = current_time + process.remaining_time
                        process.remaining_time = 0
                            
                        #append completion time to original list
                        index = [i for i, p in enumerate(processes) if p.process_num == process.process_num][0]
                        processes[index].completion_time = end_time
                            
                        copy_list.remove(process)
                        if process in queued_list:
                            queued_list.remove(process)
                        

                    #append to sequence list
                    start_time = current_time
                    sequence_list.append((process.process_num, start_time, end_time))
                    current_time = end_time
                
    print_ganttchart(sequence_list)                
    return processes  
            
#ganttchart
def print_ganttchart(sequence_list):
    print()
    print("Gantt Chart:")
    print("|", end=" ")
    for p in sequence_list:
        if p[0] == "idle":
            print(f"{p[0]} ({p[1]} - {p[2] + 1}) |", end=" ")       
        else:
            print(f"P{p[0]} ({p[1]} - {p[2]}) |", end=" ")  
    print()                   
            
        
# !! Where program starts !!
        
print()
print("Multilevel Queue CPU Scheduling Algorithm")
print()

print("Select the algorithms (choose the number):")
print("1. First Come First Serve")
print("2. Shortest Job First")
print("3. Priority Non-Preemptive")
print("4. Shortest Remaining Time First")
print("5. Priority Preemptive")
print("6. Round-Robin")
print()

#'''      
#use this to include user input
#ask for queue 1, queue 2 and time quantum
time_quantum = 0
top_queue = int(input("Enter the algorithm for queue 1: "))
bottom_queue = int(input("Enter the algorithm for queue 2: "))
if top_queue == 6 or bottom_queue == 6:
    time_quantum = int(input("Enter the the time quantum: "))

#ask for process details
num_of_processes = int(input("Enter the number of processes included: "))
processes = []
for x in range(1, num_of_processes + 1):
    processes.append(input_process(x))
 
#'''

'''
#testing algo without input
processes = [
        Process(1, 8, 4, 2, 1),
        Process(2, 5, 9, 1, 1),
        Process(3, 1, 4, 2, 1),
        Process(4, 6, 3, 1, 1),
        Process(5, 7, 6, 1, 1)
    ]
num_of_processes = 5
top_queue = 6
bottom_queue = 1
time_quantum = 3
'''
'''
#test case 2
q1
processes = [
        Process(1, 3, 4, 2, 1),
        Process(2, 5, 9, 1, 1),
        Process(3, 8, 4, 2, 2),
        Process(4, 0, 7, 1, 2),
        Process(5, 12, 6, 1, 1)
    ]
num_of_processes = 5
top_queue = 3
bottom_queue = 4
'''
    
#rearrangement of process based on algo // SJF
new_sequence = mlq_algo(processes, top_queue, bottom_queue, time_quantum)

display_table(processes)
avg_tt(processes)
avg_wt(processes)
cpu_util(processes)