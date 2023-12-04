import matplotlib.pyplot as plt

def plot_points(x, y, seek_time):
    plt.scatter(x, y, color='blue', marker='o', label='Points')
    plt.plot(x, y, color='red', linestyle='-', linewidth=1, label='Connect the Dots')
    
    for i, txt in enumerate(y):
        plt.text(x[i], y[i], f'({x[i]})', ha='right', va='bottom')

    plt.title('Shortest Seek Time First')
    plt.xlabel(f'Seek Time: {seek_time}')
    plt.ylabel('Number of points')
    plt.gca().invert_yaxis()  
    plt.grid(True)
    plt.legend()
    plt.show()

def shortest_seek_time_first(current_position, requests):
    sorted_requests = sorted(requests, key=lambda req: abs(req - current_position))
    return sorted_requests

def calculate_seek_time(sequence):
    seek_time = 0
    for i in range(1, len(sequence)):
        seek_time += abs(sequence[i] - sequence[i-1])
    return seek_time

def main():
    try:
        print("[-----Shortest Seek Time First-----]")
        x_input = input("Enter points separated by spaces: ")
        x = [float(coord) for coord in x_input.split()]
        n = len(x)
        y = list(range(1, n+1))

        current_position = x[0]

        # Apply SSTF algorithm
        sorted_points = shortest_seek_time_first(current_position, x)
        seek_time = calculate_seek_time(sorted_points)

        # Plot the points, connect the dots, and add labels based on the SSTF order
        plot_points(sorted_points, y, seek_time)

    except ValueError:
        print("Invalid input. Please enter valid numbers.")

if __name__ == "__main__":
    main()

#Test case 1
#53 98 183 37 122 14 124 65 67