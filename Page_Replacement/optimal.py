import copy

class OptimalAlgorithm:
    def __init__(self, capacity):
        self.capacity = capacity
        self.queue = []  # for tracking purposes
        self.page_set = set()  # To check if the page is in
        self.frame = [] #to hold the frames for each instance
        self.page_hits = 0  # Initialize page hits counter

    def page_faults(self, pages):
        page_faults = 0
        frame_states = []
        first_instance = 0
        page_states = []
        page_logs = []

        for index, page in enumerate(pages):
            if page in self.page_set:
                self.page_hits += 1
                page_states.append('H')
                
                index_found = self.frame.index(page) + 1
                page_logs.append(['HIT', page, index_found, 3])
                
            else:
                page_faults += 1
                page_states.append('F')
                
                if len(self.page_set) < self.capacity:
                    self.page_set.add(page)
                    self.frame.append(page)
                    idx = self.frame.index(page) + 1
                    page_logs.append(['FAULT', page, idx, 1])
                else:
                    self.page_set.add(page)
                    future_indexes = {p: pages[index:].index(p) if p in pages[index:] else float('inf') for p in self.page_set}
                    page_to_replace = max(future_indexes, key=future_indexes.get)
                    idx_page_to_replace = self.frame.index(page_to_replace)
                    removed_page = self.frame[idx_page_to_replace]
                    self.frame[idx_page_to_replace] = page
                        
                    self.page_set.remove(removed_page)
                    page_logs.append(['FAULT', page, idx_page_to_replace + 1, 2, page_to_replace])
                        
            frame_states.append(list(self.frame))

        return page_faults, self.page_hits, frame_states, page_states, page_logs    


def display_frames(frames, pages, capacity, page_states):
    print("")
    print("[-----MEMORY STATE VISUALIZATION:-----]")
    print("{:<14}".format("--------------------"), end="")
    for i in range(len(frames)):
        print("{:<4}".format("-----"), end="")
    print("")
    print("{:<21}".format("| Reference String |"), end="")
    for i in range(len(pages)):
        print("{:<2} {:<2}".format(pages[i], "|"), end="")
    print("")    
    print("{:<14}".format("--------------------"), end="")
    for i in range(len(frames)):
        print("{:<4}".format("-----"), end="")
    print("")

    # Find the maximum length of frames to determine the number of -1s to add
    max_length = max(len(frame) for frame in frames)
    for i in range(max_length):
        print("{:<21}".format("| Frame #{}         |".format(i + 1)), end="")
        for frame in frames:
            if i < len(frame):
                print("{:<2} {:<2}".format(frame[i], "|"), end="")
            else:
                print("{:<2} {:<2}".format("-", "|"), end="")
        print("")
    print("{:<14}".format("--------------------"), end="")
    for i in range(len(frames)):
        print("{:<4}".format("-----"), end="")
    print("")
    print("{:<21}".format("| Status           |"), end="")
    for i in range(len(page_states)):
        print("{:<2} {:<2}".format(page_states[i], "|"), end="")
    print("") 
    print("{:<14}".format("--------------------"), end="")
    for i in range(len(frames)):
        print("{:<4}".format("-----"), end="")
    print("") 
    
def displayLogs (page_logs):
    print("")
    print("[-----PAGE REPLACEMENT LOGS-----]")
    for index, sublist in enumerate(page_logs, start=1):
        if sublist[3] == 1:
            print(f"{index:<3} ❌ {sublist[0]:<6} : Page {sublist[1]} placed in frame {sublist[2]}")
        elif sublist[3] == 2:
            print(f"{index:<3} ❌ {sublist[0]:<6} : Page {sublist[1]} replaced Page {sublist[4]} in frame {sublist[2]}")
        elif sublist[3] == 3:
            print(f"{index:<3} 💥 {sublist[0]:<6} : Page {sublist[1]} found in frame {sublist[2]}")

def performanceMetrics(fault, hit):
    total = fault + hit
    print("")
    print("[-----PERFORMANCE METRICS-----]")
    print(f"No. of Faults: {fault:<20}", end="")
    print(f"No. of Hits: {hit}")
    fault_r = fault / total * 100
    hit_r = hit / total * 100
    print(f"Fault Percentage: {fault_r:.2f}%{'' :<11}", end="")
    print(f"Hit Percentage: {hit_r:.2f}%")
    print("")
    return fault_r, hit_r
    
def summaryStatistics(fault, hit, fault_r, hit_r, capacity):
    print("")
    print("[-----SUMMARY STATISTICS-----]")
    print("-------------------------------------------------------------------------------------")
    print("| {:<27}| {:<11}| {:<5}| {:<7}| {:<10}| {:<12}|".format("Page Replacement Algorithm", "Frame Size", "Hits", "Faults", "Hit Ratio", "Fault Ratio"))    
    print("-------------------------------------------------------------------------------------")
    print("| {:<27}| {:<11}| {:<5}| {:<7}| {:<8.2f}% | {:<10.2f}% |".format("Optimal Page Replacement", capacity, hit, fault, hit_r, fault_r))
    print("-------------------------------------------------------------------------------------")
    print("")
    
    
def integrate_optimal_algorithm(capacity, pages):
    optimal = OptimalAlgorithm(capacity)
    faults, hits, frame_states, page_states, page_logs = optimal.page_faults(pages)

    display_frames(frame_states, pages, capacity, page_states)
    displayLogs(page_logs)
    fault_r, hit_r = performanceMetrics(faults, hits)
    summaryStatistics(faults, hits, fault_r, hit_r, capacity)



print("")
print("")
print("[-----OPTIMAL PAGE REPLACEMENT ALGORITHM-----]")
print("")

'''
# Example usage:
#test case 1
capacity = 3  # Define the capacity of the page frame
pages = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2]  # Reference string of pages
# 7 0 1 2 0 3 0 4 2 3 0 3 2

#test case 2
capacity = 3
pages = [7, 0, 1, 2, 0, 3, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7]
# 7 0 1 2 0 3 4 2 3 0 3 2 1 2 0 1 7
'''

input_string = input("Enter the reference string: ")
numbers_as_strings = input_string.split()
pages = [int(num) for num in numbers_as_strings]

capacity = int(input("Enter the number of frames: "))
#'''
integrate_optimal_algorithm(capacity, pages)
