import random
import csv
import time
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle


def check_answers():
    player_sums = [int(entry.get()) if entry.get() !=
                   '' else 9999 for entry in entries]
    totals_row = [x+y for x in row_indices for y in column_headers]
    print(f'''Player entered: {player_sums}
    Correct answers are:{totals_row}
    '''
          )

    for i, entry in enumerate(entries):
        if player_sums[i] == totals_row[i]:  # Use modulus to get the correct column index
            entry.config(style="CorrectEntry.TEntry")
        else:
            entry.config(style="WrongEntry.TEntry")

    correct = all(player_sums[j] == totals_row[j]
                  for j in range(grid_size * grid_size))
    end_time = time.time()
    elapsed_time = round(end_time - start_time, 2)

    if correct:
        system_time = time.strftime("%Y-%m-%d %H:%M:%S")
        session_time = elapsed_time
        time_per_sum = elapsed_time / (grid_size * grid_size)

        # Update the CSV log file
        log_data = [system_time, session_time, time_per_sum]

        try:
            with open("log_file.csv", "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(log_data)
        except IOError:
            with open("log_file.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(
                    ["System Time", "Session Time", "Time per Sum"])
                writer.writerow(log_data)
    else:
        pass


def create_grid():
    global entries, column_headers, row_indices, grid_size

    # Set up the grid and initialize variables
    column_headers = [random.randint(10, 99) for _ in range(grid_size)]
    row_indices = [random.randint(10, 99) for _ in range(grid_size)]

    # Create column headers
    for j in range(grid_size):
        column_header_label = ttk.Label(
            frame, text=column_headers[j], style="ColumnHeader.TLabel")
        column_header_label.grid(row=0, column=j+1)

    entries = []

    # Create grid cells and row indices
    for i in range(grid_size):
        row_index_label = ttk.Label(
            frame, text=row_indices[i], style="RowIndex.TLabel")
        row_index_label.grid(row=i+1, column=0)

        for j in range(grid_size):
            entry = ttk.Entry(frame, width=5, style="Default.TEntry")
            entry.grid(row=i+1, column=j+1)
            entries.append(entry)


def start_game():
    create_grid()
    global start_time
    start_time = time.time()


grid_size = 10

# Create the main window
window = tk.Tk()
window.title("Grid Game")

# Apply the themed style to the window
style = ThemedStyle(window)
style.theme_use("clam")

# Configure style options
style.configure("TLabel", padding=5, font=("Helvetica", 12))
style.configure("TEntry", padding=5, font=("Helvetica", 12))
style.configure("CorrectEntry.TEntry", fieldbackground="#CCFFCC")
style.configure("WrongEntry.TEntry", fieldbackground="#FFCCCC")
style.configure("ColumnHeader.TLabel",
                background="lightgray", foreground="black")
style.configure("RowIndex.TLabel", background="lightgray", foreground="black")

# Create a frame to hold the grid
frame = ttk.Frame(window)
frame.pack(padx=10, pady=10)

# Create a button frame to hold the buttons
button_frame = ttk.Frame(window)
button_frame.pack()

# Create a button to start the game
start_button = ttk.Button(button_frame, text="Start Game", command=start_game)
start_button.pack(side="left", padx=5)

# Create a button to check answers
check_button = ttk.Button(
    button_frame, text="Check Answers", command=check_answers)
check_button.pack(side="left", padx=5)


# Calculate the required window size
grid_width = grid_size * 50  # Assuming each cell is 50 pixels wide
grid_height = grid_size * 30  # Assuming each cell is 30 pixels high
button_frame.update()
button_frame_height = max(start_button.winfo_height(),
                          check_button.winfo_height())
button_frame_width = button_frame.winfo_width()
window_width = grid_width + button_frame_width + 20  # Adding padding
window_height = grid_height + button_frame_height + \
    80  # Adding padding and spacing

print(
    f'''Grid width: {grid_width}, Grid height: {grid_height}, Button Frame width: {button_frame_width}, Button Frame height: {button_frame_height}''')
# Set the window size
window.geometry(f"{window_width}x{window_height}")

# Start the Tkinter event loop
window.mainloop()
