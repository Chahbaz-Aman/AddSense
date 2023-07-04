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
        system_time = time.strftime("%d-%m-%Y %H:%M")
        session_time = elapsed_time
        time_per_sum = elapsed_time / (grid_size * grid_size)

        # Update the CSV log file
        log_data = [str(system_time), str(session_time), str(time_per_sum)]

        try:
            with open("log_file.csv", "a", newline="") as file:
                # writer = csv.writer(file)
                file.write(','.join(log_data)+'\n')
                # writer.writerow(log_data)
        except IOError:
            with open("log_file.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(log_data)
    else:
        pass


def create_grid():
    global entries, column_headers, row_indices, grid_size
    grid_size = int(grid_size_selector.get())

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


def clear_grid():
    # Remove any existing grid elements
    for widget in frame.winfo_children():
        widget.destroy()


def start_game():
    clear_grid()
    create_grid()
    global start_time
    start_time = time.time()


def increase_size():
    current_size = int(grid_size_selector.get())
    if current_size < max_size:
        grid_size_selector.set(str(current_size + 2))


def decrease_size():
    current_size = int(grid_size_selector.get())
    if current_size > min_size:
        grid_size_selector.set(str(current_size - 2))


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

# Define the minimum and maximum grid sizes
min_size = 2
max_size = 10

# Create the grid size variable
grid_size_selector = tk.StringVar()
grid_size_selector.set(str(max_size))

# Create the grid size label
size_label = ttk.Label(button_frame, text="Grid Size:")
size_label.pack(side="left", padx=(0, 5))

# Create the decrease button
decrease_button = ttk.Button(
    button_frame, text="\u25bc", command=decrease_size)
decrease_button.pack(side="left")

# Create the grid size display label
size_display_label = ttk.Label(button_frame, textvariable=grid_size_selector)
size_display_label.pack(side="left")

# Create the increase button
increase_button = ttk.Button(
    button_frame, text="\u25b2", command=increase_size)
increase_button.pack(side="left")

# Create a button to start the game
start_button = ttk.Button(button_frame, text="Start Game", command=start_game)
start_button.pack(side="left", padx=5)

# Create a button to check answers
check_button = ttk.Button(
    button_frame, text="Check Answers", command=check_answers)
check_button.pack(side="left", padx=5)


# Calculate the required window size
grid_width = 0 * 50  # Assuming each cell is 50 pixels wide
grid_height = 10 * 30  # Assuming each cell is 30 pixels high
button_frame.update()
button_frame_height = max(start_button.winfo_height(),
                          check_button.winfo_height())
button_frame_width = button_frame.winfo_width()
window_width = grid_width + button_frame_width + 20  # Adding padding
window_height = grid_height + button_frame_height + \
    80  # Adding padding and spacing

# print(
#     f'''Grid width: {grid_width}, Grid height: {grid_height}, Button Frame width: {button_frame_width}, Button Frame height: {button_frame_height}''')
# Set the window size
window.geometry(f"{window_width}x{window_height}")

# Start the Tkinter event loop
window.mainloop()
