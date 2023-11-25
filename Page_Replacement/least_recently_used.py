#LRU page replacement algorithm 

def LeastRecentlyUsed(frames, referenceString):
    arr = [] #This two dimensional array holds the dimensional array of page replacement
    pageFault = [''] * len(referenceString)  #This holds the page fault if hit or not
    counter = [] #This is a one dimensional array that counts the least used per frame

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
        
        #Change this code
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
            if x >= 2 and referenceString[x] == arr[y][x]:
                replacer = y
                counter[y] = 0
                fcfs = 0
                pageFault[x] = 'H'
                break
            elif testCase < counter[y]:
                testCase = counter[y]
                replacer = y
                fcfs = 0
                smaller = 0
            elif arr[y][x] == -1:
                replacer = y
                fcfs = 0
                break
            
        arr[replacer][x] = referenceString[x]

        if smaller == 0:
            counter[replacer] = 0
        elif fcfs == -1:
            counter[replacer] = 0

    displayFrames(arr, referenceString, frames, pageFault)


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






