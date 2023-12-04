import matplotlib.pyplot as plt
import copy

def get_input():
    print("[-----C-SCAN (Circular SCAN) Algorithm-----]")
    num_cylinders = int(input("Enter the number of cylinders: "))
    numbers_input = input("Enter points separated by spaces: ")
    reference_list = list(map(int, numbers_input.split()))
    return reference_list, num_cylinders

def c_scan_io_management(sequence, initial_head, cylinders):
    sorted_sequence = sorted(sequence)
    index = sorted_sequence.index(initial_head)
    n = len(sorted_sequence)
    new_sequence = []

    # Service requests in increasing order until the end of the disk
    for i in range(index, n):
        new_sequence.append(sorted_sequence[i])
        if i == n - 1:
            new_sequence.append(cylinders - 1)
            new_sequence.append(0)
        

    # Jump to the beginning and continue servicing requests until reaching initial head position
    for i in range(0, index):
        new_sequence.append(sorted_sequence[i])

    return new_sequence
    
def plot_sequence(numbers, seek_time, num_cylinders):
    y_values = range(1, len(numbers) + 1)  # Use range as y-values
    
    plt.scatter(numbers, y_values, color='blue', marker='o', label='Points')
    plt.plot(numbers, y_values, color='red', linestyle='-', linewidth=1, label='Connect the Dots')
    
    for i, txt in enumerate(numbers):
        plt.text(numbers[i], y_values[i], f'({numbers[i]})', ha='right', va='bottom')
    
    plt.yticks(range(1, len(numbers) + 1))
    
    plt.title('C-SCAN (Circular SCAN) Algorithm')
    plt.xlabel(f'Seek Time: {seek_time}')
    plt.ylabel('Number of Points')
    plt.xlim(0, num_cylinders)
    plt.gca().invert_yaxis()  # Invert y-axis to display in reverse
    plt.grid(True)
    
    row1, row2, seektime = get_seektime(sequence)
    # Adding text below the plot with line breaks
    combined_text = row1 + '\n' + row2 + '\n' + f'Total Seek Time: {seektime}'
    plt.figtext(0.5, 0.01, combined_text, fontsize=12, color='blue', ha='center', va='bottom')
    
    plt.legend()
    plt.show()


def get_seektime(sequence):
    print()
    print("Seek Time Calculation:")
    sub_seektime = []
    first_calc = ''
    second_calc = ''
    seektime = 0
    for i in range(len(sequence) - 1):
        if sequence[i] > sequence[i+1]:
            if i != (len(sequence)-2):
                first_calc += f"({sequence[i]} - {sequence[i+1]}) + "
            else:
                first_calc += f"({sequence[i]} - {sequence[i+1]})"
            difference = sequence[i] - sequence[i+1]
        else:
            if i != (len(sequence)-2):
                first_calc += f"({sequence[i+1]} - {sequence[i]}) + "
            else:
                first_calc += f"({sequence[i+1]} - {sequence[i]})"
            difference = sequence[i+1] - sequence[i]
        sub_seektime.append(difference)
    for i, num in enumerate(sub_seektime):
        if i != (len(sub_seektime)-1):
            second_calc += f"{num} + "
        else:
            second_calc += f"{num}"
        seektime += num
    print(first_calc)
    print(second_calc)
    print(f"Seektime: {seektime}")
    print()
    return first_calc, second_calc, seektime

def display_sequence(sequence):
    #Display the sequences of numbers
    print("Sequence of Numbers:")
    for i, num in enumerate(sequence, start=1):
        print(f"Step {i}: {num}")

# Perform the Functions
ref_string, cylinders = get_input()
starting_head = ref_string[0]
sequence = c_scan_io_management(ref_string, starting_head,cylinders)
r1, r2, st = get_seektime(sequence)
plot_sequence(sequence, st, cylinders)

'''
# Static
ref_string = [65, 117, 58, 112, 7, 101, 73, 105, 38, 88]
sequence = fcfs_io_management(ref_string)
r1, r2, st = get_seektime(sequence)
plot_sequence(sequence, st)

# test case
ref_string = [65, 117, 58, 112, 7, 101, 73, 105, 38, 88]
65 117 58 112 7 101 73 105 38 88
'''