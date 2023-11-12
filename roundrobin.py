class RoundRobin:
    @staticmethod
    def schedulingProcess(process_data, time_slice):
        start_time = []
        exit_time = []
        executed_process = []
        ready_queue = []
        s_time = 0
        min_arrival_time = float('inf')
        process_data.sort(key=lambda x: x[1])

        # Find the smallest arrival time
        for i in range(len(process_data)):
            if process_data[i][1] < min_arrival_time:
                min_arrival_time = process_data[i][1]

        # Initialize the last two columns of process_data
        for i in range(len(process_data)):
            process_data[i].extend([0, process_data[i][2]])

        while 1:
            normal_queue = []
            temp = []
            for i in range(len(process_data)):
                if process_data[i][1] <= s_time and process_data[i][3] == 0:
                    present = 0
                    if len(ready_queue) != 0:
                        for k in range(len(ready_queue)):
                            if process_data[i][0] == ready_queue[k][0]:
                                present = 1

                    if present == 0:
                        temp.extend([process_data[i][0], process_data[i][1], process_data[i][2], process_data[i][4]])
                        ready_queue.append(temp)
                        temp = []

                    if len(ready_queue) != 0 and len(executed_process) != 0:
                        for k in range(len(ready_queue)):
                            if ready_queue[k][0] == executed_process[len(executed_process) - 1][0]:
                                ready_queue.insert((len(ready_queue) - 1), ready_queue.pop(k))

                elif process_data[i][3] == 0:
                    temp.extend([process_data[i][0], process_data[i][1], process_data[i][2], process_data[i][4]])
                    normal_queue.append(temp)
                    temp = []

            if len(ready_queue) == 0 and len(normal_queue) == 0:
                break

            if len(ready_queue) != 0:
                if ready_queue[0][2] > time_slice:
                    start_time.append(s_time)
                    s_time = s_time + time_slice
                    e_time = s_time
                    exit_time.append(e_time)
                    executed_process.append((ready_queue[0][0], s_time))
                    for j in range(len(process_data)):
                        if process_data[j][0] == ready_queue[0][0]:
                            break
                    process_data[j][2] = process_data[j][2] - time_slice
                    ready_queue.pop(0)
                elif ready_queue[0][2] <= time_slice:
                    start_time.append(s_time)
                    s_time = s_time + ready_queue[0][2]
                    e_time = s_time
                    exit_time.append(e_time)
                    executed_process.append((ready_queue[0][0], s_time))
                    for j in range(len(process_data)):
                        if process_data[j][0] == ready_queue[0][0]:
                            break
                    process_data[j][2] = 0
                    process_data[j][3] = 1
                    process_data[j].append(e_time)
                    ready_queue.pop(0)
            elif len(ready_queue) == 0:
                if s_time < normal_queue[0][1]:
                    s_time = normal_queue[0][1]
                if normal_queue[0][2] > time_slice:
                    start_time.append(s_time)
                    s_time = s_time + time_slice
                    e_time = s_time
                    exit_time.append(e_time)
                    executed_process.append((normal_queue[0][0], s_time))
                    for j in range(len(process_data)):
                        if process_data[j][0] == normal_queue[0][0]:
                            break
                    process_data[j][2] = process_data[j][2] - time_slice
                elif normal_queue[0][2] <= time_slice:
                    start_time.append(s_time)
                    s_time = s_time + normal_queue[0][2]
                    e_time = s_time
                    exit_time.append(e_time)
                    executed_process.append((normal_queue[0][0], s_time))
                    for j in range(len(process_data)):
                        if process_data[j][0] == normal_queue[0][0]:
                            break
                    process_data[j][2] = 0
                    process_data[j][3] = 1
                    process_data[j].append(e_time)


        t_time = RoundRobin.calculateTurnaroundTime(process_data)
        w_time = RoundRobin.calculateWaitingTime(process_data)
        
        RoundRobin.ganttChart(executed_process, min_arrival_time)
        RoundRobin.printData(process_data, t_time, w_time, time_slice)

        max_completed_time = executed_process[-1][1] #Get max value for CPU scheduling 

        RoundRobin.cpu_util(min_arrival_time, max_completed_time)
        
    @staticmethod
    def ganttChart(executed_process, min_arrival_time):

        print(f'Gantt Chart:')
        start_index = 0

        for i in range(len(executed_process) - 1):
            if (min_arrival_time != 0):
                if (min_arrival_time == 1):
                    print(f'idle ({0} - {1})', end=" | ")
                    start_index = min_arrival_time + 1
                    min_arrival_time = 0
                else:
                    print(f'idle ({0} - {min_arrival_time})', end=" | ")
                    start_index = min_arrival_time + 1
                    min_arrival_time = 0
            if (start_index == 0):
                if (start_index == executed_process[i][1] - 1):
                    print(f'P{executed_process[i][0]} ({0})', end=" | ")
                    start_index = executed_process[i][1] + 1
                else:
                    print(f'P{executed_process[i][0]} ({0} - {executed_process[i][1]})', end=" | ")
                    start_index = executed_process[i][1] + 1
            else:
                if (start_index == executed_process[i][1]):
                    print(f'P{executed_process[i][0]} ({start_index - 1}) - ({start_index})', end=" | ")
                    start_index = executed_process[i][1] + 1
                else:
                    print(f'P{executed_process[i][0]} ({start_index - 1} - {executed_process[i][1]})', end=" | ")
                    start_index = executed_process[i][1] + 1

        # Print the last process separately
        if (start_index == executed_process[-1][1]):
            print(f'P{executed_process[-1][0]} ({start_index})')
        else:
            print(f'P{executed_process[-1][0]} ({start_index} - {executed_process[-1][1]})')


    @staticmethod
    def calculateTurnaroundTime(process_data):
        total_turnaround_time = 0
        for i in range(len(process_data)):
            turnaround_time = process_data[i][5] - process_data[i][1]
            total_turnaround_time = total_turnaround_time + turnaround_time
            process_data[i].append(turnaround_time)
        average_turnaround_time = total_turnaround_time / len(process_data)
        return average_turnaround_time

    @staticmethod
    def calculateWaitingTime(process_data):
        total_waiting_time = 0
        for i in range(len(process_data)):
            waiting_time = process_data[i][6] - process_data[i][4]
            total_waiting_time = total_waiting_time + waiting_time
            process_data[i].append(waiting_time)
        average_waiting_time = total_waiting_time / len(process_data)
        return average_waiting_time

    @staticmethod
    def cpu_util(min_arrival_time, max_completed_time):
        utilization = ((max_completed_time - min_arrival_time) / max_completed_time) * 100
        print(f"CPU Utilization: {utilization:.2f}%")

    @staticmethod
    def printData(process_data, average_turnaround_time, average_waiting_time, time_slice):
        process_data.sort(key=lambda x: x[0])
        print("Process Number  Arrival Time  Burst Time  Time Quantum  Completion Time  Turnaround Time  Waiting Time")
        for i in range(len(process_data)):
            print("{:<15} {:<14} {:<11} {:<14} {:<17} {:<17} {:<12}".format(
                process_data[i][0], process_data[i][1], process_data[i][4], time_slice,
                process_data[i][5], process_data[i][6], process_data[i][7]))
        print(f'Average Turnaround Time: {average_turnaround_time}')
        print(f'Average Waiting Time: {average_waiting_time}')

if __name__ == "__main__":
    processes_test = [
        [1, 3, 4],
        [2, 5, 9],
        [3, 8, 4],
        [4, 0, 7],
        [5, 12, 6]
    ]

    time_quantum = 3

    RoundRobin.schedulingProcess(processes_test, time_quantum)

    # Second Test Case
    # [1, 3, 4],
    # [2, 5, 9],
    # [3, 8, 4],
    # [4, 0, 7],
    # [5, 12, 6]

    # time_quantum = 3

    #Third Test Case
    # [1, 2, 10],
    # [2, 13, 9],
    # [3, 20, 7],
    # [4, 1, 3],
    # [5, 11, 11]

    # time_quantum = 3
