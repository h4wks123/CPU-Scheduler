import matplotlib.pyplot as plt

def plot_points(x, y, seek_time, num_cylinders, formula):
    plt.scatter(x, y, color='blue', marker='o', label='Points')
    plt.plot(x, y, color='red', linestyle='-', linewidth=1, label='Connect the Dots')
    
    for i, txt in enumerate(y):
        plt.text(x[i], y[i], f'({x[i]})', ha='right', va='bottom')

    plt.title('C-Look Scheduling Algorithm')
    plt.xlabel(f'Seek Time: {seek_time}')
    plt.ylabel('Number of Cylinders')
    plt.xlim(0, num_cylinders)
    plt.gca().invert_yaxis()  
    plt.grid(True)
    plt.figtext(0.5, 0.01, formula, fontsize=12, color='blue', ha='center', va='bottom')
    plt.show()

def c_look_scheduling_algorithm(current_position, requests):
    temp = sorted(requests)
    sorted_requests = []

    # Find the index of current_position in the sorted list
    index_current_position = temp.index(current_position)

    # Scan from current_position to the end
    for i in range(index_current_position, len(temp)):
        sorted_requests.append(temp[i])

    # Scan from the beginning to current_position
    smallest_val = 0
    for i in range(0, index_current_position):
        sorted_requests.append(temp[i])
        if smallest_val < temp[i]:
            smallest_val = temp[i]

    return sorted_requests, smallest_val


def calculate_seek_time(current_position, sequence, smallest_val):
    seek_time = (max(sequence) - current_position) + (max(sequence) - min(sequence)) + (smallest_val - min(sequence))
    return seek_time

def generate_formula(current_position, sequence, seek_time, smallest_val):
    formula_str = []  
    formula_str.append(f'({int(max(sequence))} - {int(current_position)}) + ({int(max(sequence))} - {(int(min(sequence)))}) + ({int(smallest_val)} - {int(min(sequence))})= {int(seek_time)}')
    return ' '.join(formula_str)

def main():
    try:
        print("[-----C-Look Scheduling Algorithm-----]")

        num_cylinders = int(input("Enter the number of cylinders: "))

        x_input = input("Enter points separated by spaces: ")
        x = [float(coord) for coord in x_input.split()]
        n = len(x)
        y = list(range(1, n+1))

        current_position = x[0]

        # Apply SSTF algorithm
        sorted_points, smallest_val = c_look_scheduling_algorithm(current_position, x)
        seek_time = calculate_seek_time(current_position, sorted_points, smallest_val)
        formula = generate_formula(current_position, sorted_points, seek_time, smallest_val)

        # Plot the points, connect the dots, and add labels based on the SSTF order
        plot_points(sorted_points, y, seek_time, num_cylinders, formula)

    except ValueError:
        print("Invalid input. Please enter valid numbers.")

if __name__ == "__main__":
    main()

#Test case 1
#53 98 183 37 122 14 124 65 67

#Test case 2
#55 93 176 42 148 27 14 180