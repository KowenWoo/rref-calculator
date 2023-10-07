'''
reduced row echelon calculator
'''
import tkinter as tk
import numpy as np

def create_grid(w, h):
    global entries
    entries = []

    frame = tk.Frame(root)
    frame.grid(row = 4, sticky = "NSEW")
    
    if w <= 0 or h <= 0:
        for widget in root.winfo_children():
            widget.destroy()
        error = tk.Label(root, text = "ERROR: enter positive integers only")
        error.grid(column = 0, row = 0)
        root.after(3000, main())

    for i in range(h):
        row = []
        for j in range(w):
            entry = tk.Entry(frame, width=5)
            entry.grid(row=i + 4, column=j, padx=0)
            row.append(entry)
        entries.append(row)

    # Calculate the new window size based on the grid dimensions
    new_width = w * 50
    new_height = (h + 3) * 30
    root.geometry(f"{new_width}x{new_height}")

def submit():
    matrix = []
    for row in entries:
        row_values = [float(entry.get()) for entry in row]
        matrix.append(row_values)
    
    # Convert the matrix to NumPy array for manipulation
    matrix = np.array(matrix)
    
    # Perform Gaussian Elimination to obtain RREF
    rref_matrix = gaussian_elimination(matrix)
    
    # Display the RREF matrix in the Entry widgets
    for i in range(len(rref_matrix)):
        for j in range(len(rref_matrix[0])):
            entries[i][j].delete(0, tk.END)
            entries[i][j].insert(0, str(rref_matrix[i][j]))

def gaussian_elimination(matrix):
    rows, cols = matrix.shape
    r = 0
    
    for c in range(cols):
        pivot_row = None
        for i in range(r, rows):
            if matrix[i][c] != 0:
                pivot_row = i
                break
        
        if pivot_row is not None:
            matrix[[r, pivot_row]] = matrix[[pivot_row, r]]  # Swap rows
            matrix[r] = matrix[r] / matrix[r][c]  # Normalize pivot row
            
            for i in range(rows):
                if i != r:
                    factor = matrix[i][c]
                    matrix[i] = matrix[i] - factor * matrix[r]
            
            r += 1
    
    return matrix

def main():
    global root
    root = tk.Tk()
    root.title("RREF Calculator")

    entries = []

    width_label = tk.Label(root, text="Width (w):")
    width_label.grid(row=0, column=0)

    width_entry = tk.Entry(root)
    width_entry.grid(row=0, column=1)

    height_label = tk.Label(root, text="Height (h):")
    height_label.grid(row=1, column=0)

    height_entry = tk.Entry(root)
    height_entry.grid(row=1, column=1)

    create_button = tk.Button(root, text="Create Grid", command=lambda: create_grid(int(width_entry.get()), int(height_entry.get())), padx = 5, pady = 5)
    create_button.grid(row=2, column=0, columnspan=2)

    submit_button = tk.Button(root, text="Convert to RREF", command=submit)
    submit_button.grid(row=3, column=0, columnspan=2, pady = 5, padx = 5)

    # Set column weight to 1 for all columns
    for i in range(10):  # Assuming a maximum of 10 columns, adjust as needed
        root.columnconfigure(i, weight=1)

    root.mainloop()

main()
