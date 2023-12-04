import matplotlib.pyplot as plt

def plot_points(x, y, seek_time, num_cylinders, formula):
    plt.scatter(x, y, color='blue', marker='o', label='Points')
    plt.plot(x, y, color='red', linestyle='-', linewidth=1, label='Connect the Dots')
    
    for i, txt in enumerate(y):
        plt.text(x[i], y[i], f'({x[i]})', ha='right', va='bottom')

    plt.title('Shortest Seek Time First')
    plt.xlabel(f'Seek Time: {seek_time}')
    plt.ylabel('Number of Cylinders')
    plt.xlim(0, num_cylinders)
    plt.gca().invert_yaxis()  
    plt.grid(True)
    plt.figtext(0.5, 0.01, formula, fontsize=12, color='blue', ha='center', va='bottom')
    plt.show()

def shortest_seek_time_first(current_position, requests):
    sorted_requests = [current_position]

    for _ in range(len(requests)):
        temp = -1
        num = float('inf') 
        for idx, req in enumerate(requests):
            if abs(sorted_requests[-1] - req) < num and req != -1:
                temp = idx
                num = abs(sorted_requests[-1] - req)
        if temp != -1:
            sorted_requests.append(requests[temp])
            requests[temp] = -1  
    
    if len(sorted_requests) > 1:
        sorted_requests.pop(0)

    return sorted_requests

def calculate_seek_time(sequence):
    seek_time = 0
    for i in range(1, len(sequence)):
        seek_time += abs(sequence[i] - sequence[i-1])
    return seek_time

def generate_formula(sequence, seek_time):
    formula_str = []  
    for i in range(1, len(sequence)):
        if sequence[i] > sequence[i - 1]:
            formula_str.append(f'({int(sequence[i])} - {int(sequence[i - 1])}) +')
        else:
            formula_str.append(f'({int(sequence[i - 1])} - {int(sequence[i])}) +')

    # Remove the plus sign from the last element
    if formula_str:
        formula_str[-1] = formula_str[-1].rstrip(' +')
        formula_str.append(f'= ({int(seek_time)})')

    return ' '.join(formula_str)

def main():
    try:
        print("[-----Shortest Seek Time First-----]")

        num_cylinders = int(input("Enter the number of cylinders: "))

        x_input = input("Enter points separated by spaces: ")
        x = [float(coord) for coord in x_input.split()]
        n = len(x)
        y = list(range(1, n+1))

        current_position = x[0]

        # Apply SSTF algorithm
        sorted_points = shortest_seek_time_first(current_position, x)
        seek_time = calculate_seek_time(sorted_points)
        formula = generate_formula(sorted_points, seek_time)

        # Plot the points, connect the dots, and add labels based on the SSTF order
        plot_points(sorted_points, y, seek_time, num_cylinders, formula)

    except ValueError:
        print("Invalid input. Please enter valid numbers.")

if __name__ == "__main__":
    main()

#Test case 1
#53 98 183 37 122 14 124 65 67

#Test case 2
#65 117 58 112 7 101 73 105 38 88