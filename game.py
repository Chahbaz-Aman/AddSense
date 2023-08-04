import random
import csv
import time
import pandas as pd
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle


def check_answers():
    global runs
    player_sums = [int(entry.get()) if entry.get().isnumeric()
                   else 9999 for entry in entries]
    totals_row = [x+y for x in row_indices for y in column_headers]
    # print(f'''Player entered: {player_sums}
    # Correct answers are:{totals_row}
    # '''
    #       )
    correct = all(player_sums[j] == totals_row[j]
                  for j in range(grid_size * grid_size))
    wrong = []
    for i, entry in enumerate(entries):
        if player_sums[i] == totals_row[i]:  # Use modulus to get the correct column index
            entry.config(style="CorrectEntry.TEntry")
        else:
            wrong.append(entry)

    end_time = time.time()
    elapsed_time = round(end_time - start_time, 2)

    if correct:
        system_time = time.strftime("%d-%m-%Y %H:%M")
        session_time = elapsed_time
        time_per_sum = elapsed_time / (grid_size * grid_size)

        message_frame.config(
            text=f"Congratulations! You averaged {round(time_per_sum,2)} seconds!")

        # Update the CSV log file
        log_data = [str(system_time), str(session_time), str(time_per_sum)]

        try:
            with open("log_file.csv", "a", newline="") as file:
                file.write(','.join(log_data)+'\n')
        except IOError:
            with open("log_file.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(log_data)

        runs += 1
    else:
        wrong[0].delete(0, '')
        wrong[0].focus()


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
            entry.config(style="WrongEntry.TEntry")
            entry.bind("<FocusOut>", lambda event: check_answers())
            entries.append(entry)


def clear_grid():
    # Remove any existing grid elements
    for widget in frame.winfo_children():
        widget.destroy()


def start_game():
    global start_time
    clear_grid()
    message_frame.config(text=f"Now Playing | Set Number: {runs+1}")
    create_grid()
    entries[0].focus()
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
window.title("AddSense")

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
style.configure("Message.TLabel", foreground="green", background="#F0F0F0",
                font=("Arial", 14, "bold"), justify="center")
style.configure("FrameElements.TFrame", background="#F0F0F0")

# Count number of runs today
try:
    df = pd.read_csv('log_file.csv', header=None, names=[
        'DateTime', 'Total_Time', 'Time_per_Sum'])
    df['DateTime'] = pd.to_datetime(df['DateTime'], format="%d-%m-%Y %H:%M")
    df['DateTicks'] = df['DateTime'].dt.strftime('%d %b-%y')
    system_date = time.strftime('%d %b-%y')

    runs = df[df['DateTicks'] == system_date].shape[0]
except:
    runs = 0

# Create a label to display the message
message_frame = ttk.Label(
    window, text=f"Let's test those two-digit addition skills!\nSets Completed Today: {runs}", style="Message.TLabel")
message_frame.pack(pady=10)

# Create a frame to hold the grid
frame = ttk.Frame(window)
frame.pack(padx=10, pady=10)

# Create a button frame to hold the buttons
button_frame = ttk.Frame(window, style="FrameElements.TFrame")
button_frame.pack()

# Create a button to start the game
start_button = ttk.Button(
    button_frame, text="New Game", command=start_game)
start_button.pack(side="left", padx=5)

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

# Calculate the required window size
grid_width = 0 * 50  # Assuming each cell is 50 pixels wide
grid_height = 10 * 30  # Assuming each cell is 30 pixels high
button_frame.update()
button_frame_height = start_button.winfo_height()
button_frame_width = button_frame.winfo_width()
window_width = grid_width + button_frame_width + 160  # Adding padding
window_height = grid_height + button_frame_height + \
    150  # Adding padding and spacing

# Set the window size
window.geometry(f"{window_width}x{window_height}")

# Bind the spacebar key press event to check_answers()
window.bind("<space>", lambda event: start_game())
window.bind("<KeyPress-Up>", lambda event: increase_size())
window.bind("<KeyPress-Down>", lambda event: decrease_size())

# Start the Tkinter event loop
window.mainloop()
