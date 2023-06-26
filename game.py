import random
import time
import tkinter as tk


def check_answers():
    player_sums = [int(entry.get()) for entry in entries]
    totals_row = [sum(column) for column in zip(*grid)]

    correct = all(player_sums[j] == totals_row[j] for j in range(grid_size))
    end_time = time.time()
    elapsed_time = round(end_time - start_time, 2)

    if correct:
        result_label.config(
            text=f"Congratulations! You completed the game in {elapsed_time} seconds.")
    else:
        result_label.config(text="Sorry, your answers are incorrect.")


def create_grid():
    global entries

    # Create column headers
    for j in range(grid_size):
        column_header_label = tk.Label(frame, text=column_headers[j])
        column_header_label.grid(row=0, column=j+1)

    entries = []

    # Create grid cells and row indices
    for i in range(grid_size):
        row_index_label = tk.Label(frame, text=row_indices[i])
        row_index_label.grid(row=i+1, column=0)

        for j in range(grid_size):
            entry = tk.Entry(frame, width=5)
            entry.grid(row=i+1, column=j+1)
            entries.append(entry)


def start_game():
    create_grid()
    start_time = time.time()


# Set up the grid and initialize variables
grid_size = 10
column_headers = [random.randint(10, 99) for _ in range(grid_size)]
row_indices = [random.randint(10, 99) for _ in range(grid_size)]
grid = [[0] * grid_size for _ in range(grid_size)]

# Create the main window
window = tk.Tk()
window.title("Grid Game")

# Create a frame to hold the grid
frame = tk.Frame(window)
frame.pack()

# Create a button to start the game
start_button = tk.Button(window, text="Start Game", command=start_game)
start_button.pack()

# Create a button to check answers
check_button = tk.Button(window, text="Check Answers", command=check_answers)
check_button.pack()

# Create a label to display the result
result_label = tk.Label(window)
result_label.pack()

# Start the Tkinter event loop
window.mainloop()
