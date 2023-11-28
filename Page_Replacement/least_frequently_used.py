#LRU page replacement algorithm 
import copy

def LeastFrequentlyUsed(frames, referenceString):
    arr = [] #This two dimensional array holds the dimensional array of page replacement
    referenceStringCopy = copy.deepcopy(referenceString) #This copies the reference string for FCFS
    pageFault = [''] * len(referenceString)  #This holds the page fault if hit or not
    counter = [list(set(referenceString)), [0] * len(set(referenceString))] #This is a two dimensional array that counts the least frequently used value
    pl = [''] * len(referenceString) #This one dimensional array will contain string parameters for printing the page log
    org = 0 #ReferenceStringCopy global index

    for i in range(frames):
        arr.append([-1] * len(referenceString))  # Initialize arr with -1 values
    
    for x in range(len(referenceString)):
        
        if x >= 1:
            for y in range(frames):
                if arr[y][x - 1] == -1:
                    break
                else:
                    arr[y][x] = arr[y][x - 1]

        hit = -1

        for y in range(frames): #Checks if reference String is a hit or not
            if referenceString[x] == arr[y][x]:
                for z in range(len(counter[0])):
                    if counter[0][z] == referenceString[x]:
                        counter[1][z] += 1
                        hit = 1
                        pageFault[x] = 'H'
                        pl[x] = PageReplacementLog(3, y, referenceString[x], -1)
        if hit == -1:
            
            # Get the smallest non-zero value in the specified row
            smallest_non_zero = min((value for value in counter[1] if value != 0), default=0)
            
            # For loop to look for the index with the smallest number
            referenceLib = []  # Used to hold index for FCFS or LFU
            
            if smallest_non_zero > 0:
                for y in range(len(counter[0])):
                    if counter[1][y] == smallest_non_zero:
                        referenceLib.append(counter[0][y])
                        
            #If negative 1
            if any(row[x] == -1 for row in arr):
                for y in range(frames):
                    if arr[y][x] == -1:
                        arr[y][x] = referenceString[x] 
                        pageFault[x] = 'F'
                        pl[x] = PageReplacementLog(1, y, referenceString[x], -1)
                        break
                for y in range(len(counter[0])):
                    if counter[0][y] == referenceString[x]:
                        counter[1][y] += 1
                        
            #If condition has duplicates
            elif len(referenceLib) > 1:
                
                cop = org
                holds = -1
                
                for cop in range(len(referenceStringCopy)):
                    for lib in range(len(referenceLib)):
                        if referenceStringCopy[cop] == referenceLib[lib]: 
                            for y in range(frames): #Swaps value to FCFS
                                if arr[y][x] == referenceLib[lib]:
                                    arr[y][x] = referenceString[x]
                                    pageFault[x] = 'F'
                                    pl[x] = PageReplacementLog(2, y, referenceString[x], referenceLib[lib])
                                    break
                            for y in range(len(counter[0])): #Changes val to zero
                                if counter[0][y] == referenceLib[lib]:
                                    counter[1][y] = 0
                                    break
                            for y in range(len(counter[0])): #New value becomes 1
                                if counter[0][y] == referenceString[x]:
                                    counter[1][y] = 1
                                    break
                            referenceStringCopy[cop] = -1
                            holds = 0
                    if holds == 0:
                        break
                    
                org = cop
   
            #If condition has no duplicates             
            elif len(referenceLib) == 1:
                for y in range(frames):
                    if arr[y][x] == referenceLib[0]:
                        arr[y][x] = referenceString[x]
                        pageFault[x] = 'F'
                        pl[x] = PageReplacementLog(2, y, referenceString[x], referenceLib[0])
                for z in range(len(counter[0])):
                    if counter[0][z] == referenceLib[0]:
                        counter[1][z] = 0
                    if counter[0][z] == referenceString[x]:
                        counter[1][z] += 1                        

    displayFrames(arr, referenceString, frames, pageFault)
    displayLogs(pl)
    displayMetrics(pageFault)


#Storing of Page Replacement Logs
def PageReplacementLog (pagefault, y, referenceString, arrVal):
    if pagefault == 4:
        return f"❌ FAULT  : Page {referenceString} replaced Page {arrVal} in frame #1"
    elif pagefault == 3:
        return f"💥 HIT    : Page {referenceString} found in frame #{y + 1}"
    elif pagefault == 2:
        return f"❌ FAULT  : Page {referenceString} replaced Page {arrVal} in frame #{y + 1}"
    elif pagefault == 1:
        return f"❌ FAULT  : Page {referenceString} placed in frame #{y + 1}"
    

def displayLogs (pl):
    print("")
    print("[-----PAGE REPLACEMENT LOGS-----]")
    print("")
    for index, log_message in enumerate(pl, start=1):
        print(f"{index:<3} {log_message}")
    print("")


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
print("[-----LFU PAGE REPLACEMENT ALGORITHM-----]")
print("")

input_string = input("Enter the reference string: ")
numbers_as_strings = input_string.split()
referenceString = [int(num) for num in numbers_as_strings]

frames = int(input("Enter the number of frames: "))

LeastFrequentlyUsed(frames, referenceString)


#Test Case 1
#7 0 1 2 0 3 0 4 2 3 0 3 2 1 2

#Test Case 2
#5 2 1 0 2 1 3 2 1 1 3 0 3

#Test Case 3
#7 0 1 2 0 3 4 2 3 0 3 2 1 2 0 1 7