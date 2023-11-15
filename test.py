def sort_by_arrival(processes):
    return sorted(processes, key=lambda x: x[1])

def sort_by_priority(processes):
    return sorted(processes, key=lambda x: (x[2], x[3]))

def sort_by_end(processes):
    return sorted(processes, key=lambda x: x[4])

def display_table(process_list):
    print(f"\n\n{'PID':<11}{'AT':<4}{'BT':<4}{'ET':<4}{'TT':<4}{'WT':<4}")
    print("-" * 30)
    
    for process in process_list:
        process_id, arrival_time, burst_time, end_time, turnaround_time, waiting_time = process
        print(f"P{process_id:<10}{arrival_time:<4}{burst_time:<4}{end_time:<4}{turnaround_time:<4}{waiting_time:<4}")
        print("-" * 30)

def display_metrics(process_list):
    sorted_by_end_time = sort_by_end(process_list)
    
    total_turnaround_time = sum(p[4] for p in process_list)
    total_waiting_time = sum(p[5] for p in process_list)

    print("\n\nCPU Utilization: " + str(round(total_burst_time / sorted_by_end_time[-1][3] * 100, 2)) + "%")
    print("Average Turnaround Time: " + str(round(total_turnaround_time / len(process_list), 2)) + " ms")
    print("Average Waiting Time: " + str(round(total_waiting_time / len(process_list), 2)) + " ms")

def display_chart(timeline):
    print("\n\nGantt Chart:")
    print("-" * 45)
    
    if timeline[0][1] != 0:
        print(0)
        print("     " + "idle")

    for t in timeline:
        print(t[1])
        print("     P" + str(t[0][0]))

print("--- Multilevel Feedback Queue --- \n")

num_processes = int(input("How many processes would you like to compute? "))
quantum_1 = int(input("Enter the time quantum for the first layer: "))
quantum_2 = int(input("Enter the time quantum for the second layer: "))

layer_1 = []
layer_2 = []
layer_3 = []

process_list = []
final_list = []

running_processes = []
completed_processes = []

current_time = 0
current_process_idx = 0

total_burst_time = 0
remaining_burst_time = 0

timeline = []

print("Enter the arrival time and burst time separated by spaces.\n")

for p in range(num_processes):
    init_info = input(f"P{p+1}: ")
    
    process_list.append(list(map(int, init_info.split())))
    process_list[p].insert(0, p+1)
    process_list[p].append(1)
    
    final_list.append(list(map(int, init_info.split())))
    final_list[p].insert(0, p+1)
    
    total_burst_time += process_list[p][2]

sorted_by_arrival_time = sort_by_arrival(process_list)
current_time = sorted_by_arrival_time[0][1]

remaining_burst_time = total_burst_time

while remaining_burst_time != 0:
    while sorted_by_arrival_time and sorted_by_arrival_time[0][1] <= current_time:
        layer_1.append(sorted_by_arrival_time.pop(0))
    
    if layer_1:
        if layer_1[0][3] == 1:
            if layer_1[0][2] <= quantum_1:
                current_time += layer_1[0][2]
                remaining_burst_time -= layer_1[0][2]
                
                final_list[layer_1[0][0] - 1].append(current_time)
                
                layer_1.pop(0)
            else:
                current_time += quantum_1
                
                while sorted_by_arrival_time and sorted_by_arrival_time[0][1] <= current_time:
                    layer_1.append(sorted_by_arrival_time.pop(0))
                
                layer_1[0][2] -= quantum_1
                layer_1[0][3] += 1
                layer_2.append(layer_1.pop(0))
                
                remaining_burst_time -= quantum_1
    else:
        if layer_2:
            if layer_2[0][2] <= quantum_2:
                current_time += layer_2[0][2]
                remaining_burst_time -= layer_2[0][2]
                
                final_list[layer_2[0][0] - 1].append(current_time)
                
                layer_2.pop(0)
            else:
                current_time += quantum_2
                
                while sorted_by_arrival_time and sorted_by_arrival_time[0][1] <= current_time:
                    layer_2.append(sorted_by_arrival_time.pop(0))
                
                layer_2[0][2] -= quantum_2
                layer_2[0][3] += 1
                layer_3.append(layer_2.pop(0))
                
                remaining_burst_time -= quantum_2
        elif layer_3:
            layer_3 = sort_by_arrival(layer_3)
            
            current_time += layer_3[0][2]
            remaining_burst_time -= layer_3[0][2]
            
            final_list[layer_3[0][0] - 1].append(current_time)
            
            layer_3.pop(0)
        else:
            current_time += 1
    print(current_time)

for p in range(num_processes):
    final_list[p].append(final_list[p][3] - final_list[p][1])
    final_list[p].append(final_list[p][4] - final_list[p][2])

display_table(final_list)
display_metrics(final_list)
