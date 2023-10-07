import tkinter as tk
import numpy as np
from fractions import Fraction

def create_grid(w, h):
    global entries
    entries = []

    frame = tk.Frame(root)
    frame.grid(row=4, sticky="NSEW")

    if w <= 0 or h <= 0:
        for widget in root.winfo_children():
            widget.destroy()
        error = tk.Label(root, text="ERROR: enter positive integers only")
        error.grid(column=0, row=0)
        root.after(3000, main())
        return

    for i in range(h):
        row = []
        for j in range(w):
            entry = tk.Entry(frame, width=10)  # Increased width for fractions
            entry.grid(row=i + 5, column=j, padx=0)
            row.append(entry)
        entries.append(row)

    # Calculate the new window size based on the grid dimensions
    new_width = w * 100  # Adjusted width for fractions
    new_height = (h + 3) * 30
    root.geometry(f"{new_width}x{new_height}")

def submit():
    matrix = []
    for row in entries:
        row_values = [Fraction(entry.get()) for entry in row]  # Convert to Fraction
        matrix.append(row_values)

    # Convert the matrix to NumPy array for manipulation
    matrix = np.array(matrix)

    # Check the state of the checkbox
    rref_mode = rref_var.get()

    # Perform Gaussian Elimination to obtain REF or RREF
    if rref_mode:
        result_matrix = reduced_row_echelon_form(matrix)
    else:
        result_matrix = row_echelon_form(matrix)

    # Display the result matrix in the Entry widgets
    for i in range(len(result_matrix)):
        for j in range(len(result_matrix[0])):
            entries[i][j].delete(0, tk.END)
            entries[i][j].insert(0, str(result_matrix[i][j]))  # Fractions are automatically displayed as fractions

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

def reduced_row_echelon_form(matrix):
    # Perform row echelon form first
    ref_matrix = gaussian_elimination(matrix)

    rows, cols = ref_matrix.shape

    # Backward elimination to get reduced row echelon form (RREF)
    for r in range(rows - 1, -1, -1):
        pivot_col = -1
        for c in range(cols):
            if ref_matrix[r][c] != 0:
                pivot_col = c
                break

        if pivot_col != -1:
            for i in range(r - 1, -1, -1):
                factor = ref_matrix[i][pivot_col]
                if factor != 0:
                    ref_matrix[i] = ref_matrix[i] - factor * ref_matrix[r]

    return ref_matrix

def main():
    global root
    root = tk.Tk()
    root.title("RREF Calculator")

    entries = []

    width_label = tk.Label(root, text="Width (w):")
    width_label.grid(row=0, column=0, sticky="W")

    width_entry = tk.Entry(root)
    width_entry.grid(row=0, column=1, sticky="W")

    height_label = tk.Label(root, text="Height (h):")
    height_label.grid(row=1, column=0, sticky="W")

    height_entry = tk.Entry(root)
    height_entry.grid(row=1, column=1, sticky="W")

    create_button = tk.Button(root, text="Create Grid", command=lambda: create_grid(int(width_entry.get()), int(height_entry.get())), padx=5, pady=5)
    create_button.grid(row=2, column=1, columnspan=2)

    submit_button = tk.Button(root, text="Submit Grid", command=submit)
    submit_button.grid(row=3, column=1, columnspan=2, pady=5, padx=5)

    global rref_var
    rref_var = tk.BooleanVar()
    rref_checkbox = tk.Checkbutton(root, text="RREF", variable=rref_var)
    rref_checkbox.grid(row=5, column=0, sticky="W")

    # Set column weight to 1 for all columns
    for i in range(10):  # Assuming a maximum of 10 columns, adjust as needed
        root.columnconfigure(i, weight=1)

    root.mainloop()

main()
