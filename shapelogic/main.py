import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import os

# Function to perform template matching (with colored image)
import cv2

def match_template(image, template_path):
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        raise FileNotFoundError(f"Template not found: {template_path}")
    
    # Ensure the image is in grayscale
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Ensure both image and template are of type CV_8U
    if image.dtype != template.dtype:
        image = image.astype(template.dtype)
    
    # Resize template if it is larger than the image
    if template.shape[0] > image.shape[0] or template.shape[1] > image.shape[1]:
        template = cv2.resize(template, (min(template.shape[1], image.shape[1]), min(template.shape[0], image.shape[0])))
    
    res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    return max_loc, max_val

# Function to detect shapes in the grid
def detect_shapes_in_grid(image, shape_templates, grid_size):
    edges = cv2.Canny(image, 50, 150)
    grid = []
    cell_width = image.shape[1] // grid_size
    cell_height = image.shape[0] // grid_size
    for row in range(grid_size):
        grid_row = []
        for col in range(grid_size):
            cell = edges[row * cell_height:(row + 1) * cell_height, col * cell_width:(col + 1) * cell_width]
            best_match = None
            best_match_val = -1
            for shape_name, template_path in shape_templates.items():
                _, match_val = match_template(cell, template_path)
                if match_val > best_match_val:
                    best_match = shape_name
                    best_match_val = match_val
            grid_row.append(best_match)
        grid.append(grid_row)
    return grid

# Function to solve the puzzle by finding the shape missing at the question mark
def solve_puzzle(grid, shapes):
    # Find the position of the question mark
    question_row, question_col = None, None
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "?":
                question_row, question_col = i, j
                break

    if question_row is None or question_col is None:
        return None  # No question mark found

    # Get the shapes in the same row and column, ignoring empty cells
    row_shapes = [grid[question_row][col] for col in range(len(grid)) if grid[question_row][col] != "⬜" and grid[question_row][col] != "?"]
    col_shapes = [grid[row][question_col] for row in range(len(grid)) if grid[row][question_col] != "⬜" and grid[row][question_col] != "?"]

    # Deduce the missing shape
    missing_shape = list(set(shapes) - set(row_shapes) - set(col_shapes))
    return missing_shape[0] if missing_shape else None

# Load shape templates from the shapes folder
def load_shape_templates():
    shape_templates = {}
    shape_folder = os.path.join(os.path.dirname(__file__), "shapes")
    if not os.path.exists(shape_folder):
        raise FileNotFoundError(f"The specified folder does not exist: {shape_folder}")
    for shape_name in os.listdir(shape_folder):
        if shape_name.endswith(".jpg"):
            shape_templates[shape_name.split(".")[0]] = os.path.join(shape_folder, shape_name)
    return shape_templates

# Function to open and process an image
def open_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        img = cv2.imread(file_path)
        img_resized = cv2.resize(img, (500, 500))  # Resize for display
        display_image(img_resized)
        return img_resized
    return None

# Function to display image in Tkinter window
def display_image(image):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_pil = Image.fromarray(image_rgb)
    image_tk = ImageTk.PhotoImage(image_pil)
    label.config(image=image_tk)
    label.image = image_tk  # Keep a reference

# Function to display the grid and missing shape result
def display_grid(grid, missing_shape):
    text = ""
    for row in grid:
        text += " ".join(row) + "\n"
    result_text.set(f"Detected Grid:\n{text}\n\nMissing Shape: {missing_shape}")

# Main Tkinter Application
def main():
    root = tk.Tk()
    root.title("Shape Puzzle Solver")

    # Create GUI components
    global label
    label = tk.Label(root)
    label.pack()

    # Dropdown to select grid size
    global grid_size_var
    grid_size_var = tk.IntVar(value=5)  # Default is 5x5 grid

    grid_size_label = tk.Label(root, text="Select Grid Size:")
    grid_size_label.pack()

    grid_size_dropdown = ttk.Combobox(root, textvariable=grid_size_var)
    grid_size_dropdown['values'] = (4, 5)  # Supports 4x4 or 5x5 grids
    grid_size_dropdown.pack()

    open_button = tk.Button(root, text="Open Image", command=lambda: open_puzzle(root))
    open_button.pack()

    global result_text
    result_text = tk.StringVar()
    result_label = tk.Label(root, textvariable=result_text, font=("Arial", 14))
    result_label.pack()

    root.mainloop()

# Function to open puzzle, detect shapes, and solve the puzzle
def open_puzzle(root):
    image = open_image()
    if image is None:
        return

    # Load shape templates
    shape_templates = load_shape_templates()
    shapes = list(shape_templates.keys())  # Get shape names

    # Get the selected grid size (either 4x4 or 5x5)
    grid_size = grid_size_var.get()

    # Detect shapes in the grid
    grid = detect_shapes_in_grid(image, shape_templates, grid_size)

    # Solve the puzzle
    missing_shape = solve_puzzle(grid, shapes)

    # Display the grid and the missing shape
    display_grid(grid, missing_shape)

if __name__ == "__main__":
    main()
