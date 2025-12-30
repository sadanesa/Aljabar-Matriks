import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

def identify_matrix_type(matrix):
    """nyari tau tipe matrix"""
    try:
        matrix = np.array(matrix, dtype=float)
        rows, cols = matrix.shape
        matrix_types = []
        is_square = (rows == cols)
        
        # Zero Matrix
        if np.all(matrix == 0):
            return ["Zero Matrix"]
        
        # Identity Matrix
        if is_square and np.allclose(matrix, np.eye(rows)):
            return ["Identity Matrix"]
        
        # Diagonal Matrix
        if is_square and np.allclose(matrix, np.diag(np.diag(matrix))):
            matrix_types.append("Diagonal Matrix")
            diag_elements = np.diag(matrix)
            if np.allclose(diag_elements, diag_elements[0]):
                matrix_types.append("Scalar Matrix")
        
        # Upper Triangular
        if is_square and np.allclose(matrix, np.triu(matrix)):
            matrix_types.append("Upper Triangular Matrix")
        
        # Lower Triangular
        if is_square and np.allclose(matrix, np.tril(matrix)):
            matrix_types.append("Lower Triangular Matrix")
        
        # Symmetric
        if is_square and np.allclose(matrix, matrix.T):
            matrix_types.append("Symmetric Matrix")
        
        # Skew-Symmetric
        if is_square and np.allclose(matrix, -matrix.T):
            matrix_types.append("Skew-Symmetric Matrix")
        
        # Orthogonal
        if is_square:
            product = np.dot(matrix, matrix.T)
            if np.allclose(product, np.eye(rows)):
                matrix_types.append("Orthogonal Matrix")
        
        # Singular/Non-Singular
        if is_square:
            det = np.linalg.det(matrix)
            if np.isclose(det, 0):
                matrix_types.append("Singular Matrix")
            else:
                matrix_types.append("Non-Singular Matrix")
        
        # Row/Column Matrix
        if rows == 1:
            matrix_types.append("Row Matrix")
        if cols == 1:
            matrix_types.append("Column Matrix")
        
        # Default
        if not matrix_types:
            if is_square:
                matrix_types.append("Square Matrix")
            else:
                matrix_types.append("Rectangular Matrix")
        
        return matrix_types
    except Exception as e:
        return [f"Error: {str(e)}"]


class MatrixIdentifierGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Matrix Type Identifier")
        self.root.geometry("750x650")
        
        self.entries = []
        self.rows = 3
        self.cols = 3
        
        # Main container
        container = ttk.Frame(root, padding="20")
        container.pack(fill=tk.BOTH, expand=True)
        
        # Title
        ttk.Label(container, text="Matrix Type Identifier", 
                 font=('Arial', 16, 'bold')).pack(pady=(0, 15))
        
        # Dimensions Frame
        dim_frame = ttk.LabelFrame(container, text="Matrix Size", padding="10")
        dim_frame.pack(fill=tk.X, pady=(0, 10))
        
        controls = ttk.Frame(dim_frame)
        controls.pack()
        
        ttk.Label(controls, text="Rows:").grid(row=0, column=0, padx=5)
        self.rows_var = tk.StringVar(value="3")
        ttk.Spinbox(controls, from_=1, to=10, width=8, 
                   textvariable=self.rows_var).grid(row=0, column=1, padx=5)
        
        ttk.Label(controls, text="Columns:").grid(row=0, column=2, padx=5)
        self.cols_var = tk.StringVar(value="3")
        ttk.Spinbox(controls, from_=1, to=10, width=8,
                   textvariable=self.cols_var).grid(row=0, column=3, padx=5)
        
        ttk.Button(controls, text="Create Grid", 
                  command=self.create_grid).grid(row=0, column=4, padx=10)
        
        # Matrix Input Frame
        input_frame = ttk.LabelFrame(container, text="Enter Values", padding="10")
        input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Canvas for scrolling
        canvas = tk.Canvas(input_frame, height=200)
        scrollbar = ttk.Scrollbar(input_frame, orient="vertical", command=canvas.yview)
        self.grid_frame = ttk.Frame(canvas)
        
        canvas.create_window((0, 0), window=self.grid_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.grid_frame.bind("<Configure>", 
                            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        # Buttons
        btn_frame = ttk.Frame(container)
        btn_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(btn_frame, text="🔍 Identify", 
                  command=self.identify, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Clear", 
                  command=self.clear, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Example", 
                  command=self.load_example, width=10).pack(side=tk.LEFT, padx=5)
        
        # Results
        result_frame = ttk.LabelFrame(container, text="Results", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        self.output = tk.Text(result_frame, height=10, font=('Courier', 10))
        self.output.pack(fill=tk.BOTH, expand=True)
        
        # Create initial grid
        self.create_grid()
        
        self.example_idx = 0
    
    def create_grid(self):
        """creating any grid input"""
        try:
            self.rows = int(self.rows_var.get())
            self.cols = int(self.cols_var.get())
            
            # Clear old grid
            for widget in self.grid_frame.winfo_children():
                widget.destroy()
            
            self.entries = []
            
            # Create entries
            for i in range(self.rows):
                row = []
                for j in range(self.cols):
                    e = ttk.Entry(self.grid_frame, width=10, justify='center')
                    e.grid(row=i, column=j, padx=2, pady=2)
                    e.insert(0, "0")
                    row.append(e)
                self.entries.append(row)
            
            self.output.delete(1.0, tk.END)
            self.output.insert(1.0, f"Grid created: {self.rows}×{self.cols}\nReady to identify!")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def identify(self):
        """identifying matrix"""
        try:
            # Get matrix values
            matrix = []
            for i in range(self.rows):
                row = []
                for j in range(self.cols):
                    val = self.entries[i][j].get().strip()
                    if not val:
                        val = "0"
                    row.append(float(val))
                matrix.append(row)
            
            # Identify
            types = identify_matrix_type(matrix)
            
            # Display
            result = "="*50 + "\n"
            result += "MATRIX:\n"
            result += str(np.array(matrix)) + "\n\n"
            result += "TYPES:\n"
            for i, t in enumerate(types, 1):
                result += f"{i}. {t}\n"
            result += "="*50
            
            self.output.delete(1.0, tk.END)
            self.output.insert(1.0, result)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
            self.output.delete(1.0, tk.END)
            self.output.insert(1.0, f"ERROR: {str(e)}")
    
    def clear(self):
        """clear all entries"""
        for i in range(self.rows):
            for j in range(self.cols):
                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].insert(0, "0")
    
    def load_example(self):
        """Load examples"""
        examples = [
            (3, 3, [[1,0,0],[0,1,0],[0,0,1]]),
            (3, 3, [[1,2,3],[2,4,5],[3,5,6]]),
            (3, 3, [[5,0,0],[0,3,0],[0,0,7]]),
            (3, 3, [[1,2,3],[0,4,5],[0,0,6]]),
        ]
        
        r, c, m = examples[self.example_idx]
        self.rows_var.set(str(r))
        self.cols_var.set(str(c))
        self.create_grid()
        
        for i in range(r):
            for j in range(c):
                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].insert(0, str(m[i][j]))
        
        self.example_idx = (self.example_idx + 1) % len(examples)


if __name__ == "__main__":
    root = tk.Tk()
    app = MatrixIdentifierGUI(root)
    root.mainloop()