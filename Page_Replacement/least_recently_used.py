#LRU page replacement algorithm 
import copy

def LeastRecentlyUsed(frames, referenceString):
    arr = [] #This two dimensional array holds the dimensional array of page replacement
    pageFault = [''] * len(referenceString)  #This holds the page fault if hit or not
    counter = [] #This is a one dimensional array that counts the least used per frame
    pl = [''] * len(referenceString) #This one dimensional array will contain string parameters for printing the page log

    for i in range(frames):
        arr.append([-1] * len(referenceString))  # Initialize arr with -1 values
        counter.append(0)

    for i in range(len(referenceString)):
        pageFault[i] = 'F'


    for x in range(len(referenceString)):

        if x >= 1:
            for y in range(frames):
                if arr[y][x - 1] == -1:
                    break
                else:
                    arr[y][x] = arr[y][x - 1]
        
        #all counts must be incremented before comparing
        #first priority is if there is a number that is same
        #second priority is if there is comparing the largest "counter[y]"
        #thid is if there are same largest "counter[y]" follow the process of FIFO
        
        for y in range(frames):
            if arr[y][x] == -1:
                counter[y] += 1
                break
            else:
                counter[y] += 1

        testCase = counter[0] #Compares the counter
        replacer = 0 #Holds the index of the array to replace value
        smaller = -1
        fcfs = -1
        
        for y in range(frames):
            if referenceString[x] != -1 and referenceString[x] == arr[y][x]:
                replacer = y
                counter[y] = 0
                fcfs = 0
                pageFault[x] = 'H'
                pl[x] = PageReplacementLog(3, y, referenceString[x], -1)
                break
            elif testCase < counter[y]:
                testCase = counter[y]
                replacer = y
                fcfs = 0
                smaller = 0
                pl[x] = PageReplacementLog(2, y, referenceString[x], arr[y][x])
            elif arr[y][x] == -1:
                replacer = y
                fcfs = 0
                pl[x] = PageReplacementLog(1, y, referenceString[x], -1)
                break
            
        if smaller == 0:
            counter[replacer] = 0
        elif fcfs == -1:
            counter[replacer] = 0
            pl[x] = PageReplacementLog(4, y, referenceString[x], arr[0][x])
        
        arr[replacer][x] = referenceString[x]

    displayFrames(arr, referenceString, frames, pageFault)
    displayLogs(pl)
    displayStrateTrackingLogs(arr, referenceString, frames)
    displayMetrics(pageFault)


#Storing of Page Replacement Logs
def PageReplacementLog (pagefault, y, referenceString, arrVal):
    if pagefault == 4:
        return f"FAULT  : Page {referenceString} replaced Page {arrVal} in frame #1"
    elif pagefault == 3:
        return f"HIT    : Page {referenceString} found in frame #{y + 1}"
    elif pagefault == 2:
        return f"FAULT  : Page {referenceString} replaced Page {arrVal} in frame #{y + 1}"
    elif pagefault == 1:
        return f"FAULT  : Page {referenceString} placed in frame #{y + 1}"
    
#Prints the Frame chart
def displayFrames(arr, referenceString, frames, pageFault):

    print("")
    print("[-----MEMORY STATE VISUALIZATION:-----]")
    print("")

    print("{:<14}".format("--------------------"), end="")

    for i in range(len(referenceString)):
        print("{:<4}".format("-----"), end="")

    print("")
    print("{:<21}".format("| Reference String |"), end="")

    for i in range(len(referenceString)):
        print("{:<2} {:<2}".format(referenceString[i], "|"), end="")

    print("")    
    print("{:<14}".format("--------------------"), end="")

    for i in range(len(referenceString)):
        print("{:<4}".format("-----"), end="")

    print("")      

    for x in range(frames):
        print("{:<21}".format(f"| Frame #{x + 1}         |"), end="")
        for y in range(len(referenceString)):
            if arr[x][y] == -1:
                print("{:<2} {:<2}".format("-", "|"), end="")
            else:
                print("{:<2} {:<2}".format(arr[x][y], "|"), end="")
        print("")

    print("{:<14}".format("--------------------"), end="")

    for i in range(len(referenceString)):
        print("{:<4}".format("-----"), end="")

    print("")
    print("{:<21}".format("| Status           |"), end="")

    for i in range(len(pageFault)):
        print("{:<2} {:<2}".format(pageFault[i], "|"), end="")

    print("")  
    print("{:<14}".format("--------------------"), end="")

    for i in range(len(referenceString)):
        print("{:<4}".format("-----"), end="")

    print("")


#Prints the Page Replacement Logs
def displayLogs (pl):
    print("")
    print("[-----PAGE REPLACEMENT LOGS-----]")
    print("")
    for index, log_message in enumerate(pl, start=1):
        print(f"{index:<3} {log_message}")
    print("")


#Prints the State Tracking Logs
def displayStrateTrackingLogs (arrVal, referenceString, frames):
    print("")
    print("[-----STATE TRACKING LOGS-----]")
    print(">>>LEGEND: Least Recently Used -> Most Recently Used")
    print("")
    counter = [0] * frames  # Initialize counter list with zeros
    newArrVal = copy.deepcopy(arrVal)  # Create a deep copy of arrVal

    # Use the length of the referenceString to avoid index out of range
    for x in range(len(referenceString)):

        for y in range(frames):
            if arrVal[y][x] == -1:
                counter[y] = 0
            elif x > 0 and arrVal[y][x] != arrVal[y][x - 1] and arrVal[y][x - 1] != -1:
                counter[y] = 0
            else:
                counter[y] += 1

        for y in range(frames - 1):  # Fix the loop range
            for z in range(frames - y - 1):
                temp = 0
                if counter[z] < counter[z + 1]:
                    temp = newArrVal[z][x]
                    newArrVal[z][x] = newArrVal[z + 1][x]  # Fix index
                    newArrVal[z + 1][x] = temp

    for x in range(len(referenceString)):
        print(f"[{x + 1:>2}]", end=" [")
        for y in range(frames):
            print(f"{newArrVal[y][x]:>3}", end=", " if y < frames - 1 else "  ")
        print("]")

    print("")


#Prints the Performance Metrics
def displayMetrics(pageFault):
    
    fault = hit = 0

    for i in range(len(pageFault)):
        if pageFault[i] == 'F':
            fault += 1
        else:
            hit += 1

    total = fault + hit

    print("")
    print("[-----PERFORMANCE METRICS-----]")
    print("")
    print(f"No. of Faults: {fault:<20}", end="")
    print(f"No. of Hits: {hit}")
    print(f"Fault Percentage: {fault / total * 100:.2f}%{'' :<11}", end="")
    print(f"Hit Percentage: {hit / total * 100:.2f}%")
    print("")




# Get input from the user as a string

print("")
print("[-----LRU PAGE REPLACEMENT ALGORITHM-----]")
print("")

input_string = input("Enter the reference string: ")
numbers_as_strings = input_string.split()
referenceString = [int(num) for num in numbers_as_strings]

frames = int(input("Enter the number of frames: "))

LeastRecentlyUsed(frames, referenceString)


#Test Case 1
#7 0 1 2 0 3 0 4 2 3 0 3 1 2 0

#Test Case 2
#5 2 1 0 2 1 3 2 1 1 3 0 3






