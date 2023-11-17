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

    x = i = 0
    current_time = min(x.arrival_time for x in processes)
    
    while i < len(demodataset):
        if demodataset[i].burst_time < Q1 and demodataset[i].burst_time != 0 and demodataset[i].level == 2:
            current_time += demodataset[i].burst_time
            demodataset[i].burst_time -= demodataset[i].burst_time
            demodataset[i].level -= 1
            print(demodataset[i].name, demodataset[i].burst_time, current_time, demodataset[i].level)

        else:
            if demodataset[i].level == 2 and demodataset[i].burst_time != 0:
                demodataset[i].burst_time -= Q1
                demodataset[i].level -= 1
                current_time += Q1
                print(demodataset[i].name, demodataset[i].burst_time, current_time, demodataset[i].level)

                # Check if the next process exists and if its arrival_time is less than the current_time
                if i + 1 < len(demodataset) and current_time < demodataset[i + 1].arrival_time and demodataset[i].level == 1:
                    if demodataset[x].burst_time < Q2:
                        current_time += demodataset[x].burst_time
                        demodataset[x].burst_time -= demodataset[x].burst_time
                        demodataset[x].level -= 1
                        print(demodataset[x].name, demodataset[x].burst_time, current_time, demodataset[x].level)
                    else:
                        current_time += Q2
                        demodataset[x].burst_time -= Q2
                        demodataset[x].level -= 1
                        print(demodataset[x].name, demodataset[x].burst_time, current_time, demodataset[x].level)
                    x += 1

        i += 1

    SecondQuantum(demodataset, current_time, Q2, Q3)
     

def SecondQuantum(demodataset, current_time, Q2, Q3):

    i = 0
    
    while i < len(demodataset):
        if demodataset[i].burst_time < Q2 and demodataset[i].burst_time != 0 and demodataset[i].level == 1:
            current_time += demodataset[i].burst_time
            demodataset[i].burst_time -= demodataset[i].burst_time
            demodataset[i].level -= 1
            print(demodataset[i].name, demodataset[i].burst_time, current_time, demodataset[i].level)  

        else:
            if demodataset[i].level == 1 and demodataset[i].burst_time != 0:
                demodataset[i].burst_time -= Q2
                demodataset[i].level -= 1
                current_time += Q2
                print(demodataset[i].name, demodataset[i].burst_time, current_time, demodataset[i].level)

        i += 1

    ThirdQuantum(demodataset, current_time, Q3)


def ThirdQuantum(demodataset, current_time, Q3):

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
                demodataset[i].burst_time = 0
                demodataset[i].level -= 1
                print(demodataset[i].name, demodataset[i].burst_time, current_time, demodataset[i].level)

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
                demodataset[i].burst_time = 0
                demodataset[i].level -= 1
                print(demodataset[i].name, demodataset[i].burst_time, current_time, demodataset[i].level)


if __name__ == "__main__":

    Q1 = 10
    Q2 = 15
    Q3 = 2
    data = [
        (1, 5, 30, 0, 2),
        (2, 25, 15, 0, 2),
        (3, 15, 25, 0, 2),
        (4, 10, 10, 0, 2),
        (5, 20, 35, 0, 2),
        (6, 13, 5, 0, 2)     
    ]

    result = FirstQuantum(data, Q1, Q2, Q3)


    # data = [
    #     (1, 3, 4, 0, 2),
    #     (2, 5, 9, 0, 2),
    #     (3, 8, 4, 0, 2),
    #     (4, 0, 7, 0, 2),
    #     (5, 12, 6, 0, 2)    
    # ]

    # data = [
    #     (1, 5, 14, 0, 2),
    #     (2, 8, 2, 0, 2),
    #     (3, 25, 5, 0, 2),
    #     (4, 27, 2, 0, 2),
    #     (5, 29, 2, 0, 2)    
    # ]

    # data = [
    #     (1, 5, 30, 0, 2),
    #     (2, 25, 15, 0, 2),
    #     (3, 15, 25, 0, 2),
    #     (4, 10, 10, 0, 2),
    #     (5, 20, 35, 0, 2),
    #     (6, 13, 5, 0, 2)        
    # ]
